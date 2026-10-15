#!/usr/bin/env python3
"""Create deterministic, read-only snapshots from a public WordPress REST API.

The CLI intentionally supports only the public ``posts`` and ``pages``
collections. It performs GET requests with a descriptive user agent and writes
one stable JSON array per collection; it does not read credentials or expose
any write endpoint.

Example::

    python3 scripts/snapshot-wp-rest.py \
        --base-url https://npcwoods.com \
        --output-dir content-source/wp-rest
"""

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Callable, Iterable, Mapping, Optional, Sequence
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen


RESOURCES = ("posts", "pages")
DEFAULT_BASE_URL = "https://npcwoods.com"
DEFAULT_TIMEOUT = 30.0
DEFAULT_PER_PAGE = 100
MAX_PAGES = 100
MAX_RESPONSE_BYTES = 8 * 1024 * 1024
EXCLUDED_PAGE_SLUGS = frozenset({"pay", "checkout", "cart", "my-account", "shop"})
USER_AGENT = (
    "NPCWoods-static-migration-wp-rest-snapshot/1.0 "
    "(+https://npcwoods.com/; read-only; contact: chris@npcwoods.com)"
)


class SnapshotError(RuntimeError):
    """A user-facing error while fetching or writing a snapshot."""


def _validate_base_url(base_url: str) -> str:
    parsed = urlsplit(base_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("base URL must be an absolute http(s) URL")
    if parsed.username or parsed.password:
        raise ValueError("base URL must not contain credentials")
    if parsed.query or parsed.fragment:
        raise ValueError("base URL must not contain a query or fragment")
    return base_url.rstrip("/")


def build_endpoint_url(
    base_url: str,
    resource: str,
    page: int,
    per_page: int,
) -> str:
    """Build one deterministic WordPress collection URL."""
    if resource not in RESOURCES:
        raise ValueError(f"unsupported WordPress resource: {resource}")
    if page < 1:
        raise ValueError("page must be at least 1")
    if not 1 <= per_page <= 100:
        raise ValueError("per_page must be between 1 and 100")

    base = _validate_base_url(base_url)
    query = urlencode(
        [
            ("_embed", ""),
            ("order", "asc"),
            ("orderby", "id"),
            ("page", str(page)),
            ("per_page", str(per_page)),
        ]
    )
    return f"{base}/wp-json/wp/v2/{resource}?{query}"


def _header(headers: Mapping[str, str], name: str) -> Optional[str]:
    """Read a response header case-insensitively from urllib or a test double."""
    value = headers.get(name)
    if value is not None:
        return value
    lowered = name.lower()
    for key, candidate in headers.items():
        if str(key).lower() == lowered:
            return candidate
    return None


def _fetch_page(
    url: str,
    *,
    opener: Callable[..., object],
    timeout: float,
) -> tuple[list[dict], Mapping[str, str]]:
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
        method="GET",
    )
    try:
        with opener(request, timeout=timeout) as response:
            raw = response.read(MAX_RESPONSE_BYTES + 1)
            headers = response.headers
    except HTTPError as exc:
        code = exc.code
        exc.close()
        raise SnapshotError(f"HTTP {code} while fetching {url}") from exc
    except (URLError, TimeoutError, OSError) as exc:
        reason = getattr(exc, "reason", str(exc))
        raise SnapshotError(f"network failure while fetching {url}: {reason}") from exc

    if len(raw) > MAX_RESPONSE_BYTES:
        raise SnapshotError(f"response exceeded {MAX_RESPONSE_BYTES} bytes from {url}")

    try:
        payload = json.loads(raw.decode("utf-8") if isinstance(raw, bytes) else raw)
    except (UnicodeDecodeError, TypeError, json.JSONDecodeError) as exc:
        raise SnapshotError(f"invalid JSON from {url}") from exc

    if not isinstance(payload, list) or not all(isinstance(item, dict) for item in payload):
        raise SnapshotError(f"expected a JSON array of objects from {url}")
    return payload, headers


def _stable_item_key(item: dict) -> tuple[int, object, str]:
    """Sort records by WordPress ID, with a canonical JSON fallback."""
    canonical = json.dumps(
        item,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    identifier = item.get("id")
    if isinstance(identifier, int) and not isinstance(identifier, bool):
        return (0, identifier, canonical)
    if isinstance(identifier, str) and identifier.isdigit():
        return (0, int(identifier), canonical)
    return (1, "", canonical)


def fetch_resource(
    base_url: str,
    resource: str,
    *,
    opener: Callable[..., object] = urlopen,
    timeout: float = DEFAULT_TIMEOUT,
    per_page: int = DEFAULT_PER_PAGE,
) -> list[dict]:
    """Fetch every page of a public WordPress collection."""
    if resource not in RESOURCES:
        raise ValueError(f"unsupported WordPress resource: {resource}")
    if timeout <= 0:
        raise ValueError("timeout must be greater than zero")
    if not 1 <= per_page <= 100:
        raise ValueError("per_page must be between 1 and 100")

    records: list[dict] = []
    page = 1
    while True:
        if page > MAX_PAGES:
            raise SnapshotError(f"pagination exceeded {MAX_PAGES} pages for {resource}")
        url = build_endpoint_url(base_url, resource, page, per_page)
        batch, headers = _fetch_page(url, opener=opener, timeout=timeout)
        records.extend(batch)

        total_pages_value = _header(headers, "X-WP-TotalPages")
        if total_pages_value is not None:
            try:
                total_pages = int(total_pages_value)
            except (TypeError, ValueError) as exc:
                raise SnapshotError(
                    f"invalid X-WP-TotalPages header from {url}: {total_pages_value!r}"
                ) from exc
            if total_pages < 1:
                raise SnapshotError(
                    f"invalid X-WP-TotalPages header from {url}: {total_pages_value!r}"
                )
            if total_pages > MAX_PAGES:
                raise SnapshotError(
                    f"X-WP-TotalPages exceeded {MAX_PAGES} for {resource}: {total_pages}"
                )
            if page >= total_pages:
                break
        elif len(batch) < per_page:
            break
        page += 1

    records = sorted(records, key=_stable_item_key)
    if resource == "pages":
        records = [
            record
            for record in records
            if str(record.get("slug", "")).lower() not in EXCLUDED_PAGE_SLUGS
        ]
    return records


def snapshot_resource(
    base_url: str,
    resource: str,
    output_dir: Path,
    *,
    opener: Callable[..., object] = urlopen,
    timeout: float = DEFAULT_TIMEOUT,
    per_page: int = DEFAULT_PER_PAGE,
) -> Path:
    """Fetch one resource and write its deterministic JSON snapshot."""
    records = fetch_resource(
        base_url,
        resource,
        opener=opener,
        timeout=timeout,
        per_page=per_page,
    )
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise SnapshotError(f"could not create snapshot directory {output_dir}: {exc}") from exc
    if not output_dir.is_dir():
        raise SnapshotError(f"output path is not a directory: {output_dir}")

    destination = output_dir / f"{resource}.json"
    payload = json.dumps(records, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=output_dir,
            prefix=f".{resource}.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary_path = Path(temporary.name)
            temporary.write(payload)
        os.replace(temporary_path, destination)
    except OSError as exc:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        raise SnapshotError(f"could not write snapshot {destination}: {exc}") from exc
    return destination


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Fetch deterministic, read-only WordPress posts/pages REST snapshots."
    )
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument(
        "--resource",
        dest="resources",
        action="append",
        choices=RESOURCES,
        help="resource to fetch (repeatable; defaults to posts and pages)",
    )
    parser.add_argument("--per-page", type=int, default=DEFAULT_PER_PAGE)
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    args = parser.parse_args(argv)

    resources: Iterable[str] = args.resources or RESOURCES
    try:
        for resource in resources:
            destination = snapshot_resource(
                args.base_url,
                resource,
                args.output_dir,
                timeout=args.timeout,
                per_page=args.per_page,
            )
            print(f"wrote {destination}")
    except (SnapshotError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

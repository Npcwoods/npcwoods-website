"""Unit tests for the read-only WordPress REST snapshot CLI.

These tests use mocked ``urllib`` responses and never access the network.
Run with::

    python3 -m unittest tests/test_snapshot_wp_rest.py -v
"""

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from urllib.parse import parse_qsl, urlsplit


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "snapshot-wp-rest.py"


def load_module():
    spec = importlib.util.spec_from_file_location("snapshot_wp_rest", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class FakeResponse:
    def __init__(self, payload, headers=None):
        self._payload = payload
        self.headers = headers or {}

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self, _size=-1):
        if isinstance(self._payload, bytes):
            return self._payload
        return json.dumps(self._payload).encode("utf-8")


class UrlConstructionTest(unittest.TestCase):
    def setUp(self):
        self.m = load_module()

    def test_builds_posts_and_pages_urls_with_embed_and_pagination(self):
        for resource in ("posts", "pages"):
            with self.subTest(resource=resource):
                url = self.m.build_endpoint_url(
                    "https://example.test/",
                    resource,
                    page=3,
                    per_page=25,
                )
                parsed = urlsplit(url)
                self.assertEqual(
                    parsed.path,
                    f"/wp-json/wp/v2/{resource}",
                )
                self.assertEqual(
                    dict(parse_qsl(parsed.query, keep_blank_values=True)),
                    {
                        "_embed": "",
                        "order": "asc",
                        "orderby": "id",
                        "page": "3",
                        "per_page": "25",
                    },
                )

    def test_rejects_unknown_resource(self):
        with self.assertRaises(ValueError):
            self.m.build_endpoint_url("https://example.test", "users", 1, 10)


class PaginationTest(unittest.TestCase):
    def setUp(self):
        self.m = load_module()

    def test_uses_total_pages_header_to_fetch_all_pages(self):
        responses = [
            FakeResponse([{"id": 2}], {"X-WP-TotalPages": "2"}),
            FakeResponse([{"id": 1}], {"X-WP-TotalPages": "2"}),
        ]

        def opener(request, timeout):
            self.assertEqual(timeout, 7)
            self.assertEqual(request.get_method(), "GET")
            self.assertIn("read-only", request.get_header("User-agent"))
            return responses.pop(0)

        with tempfile.TemporaryDirectory() as tmp:
            result = self.m.snapshot_resource(
                "https://example.test",
                "posts",
                Path(tmp),
                opener=opener,
                timeout=7,
                per_page=1,
            )

            self.assertEqual(result, Path(tmp) / "posts.json")
            self.assertEqual(responses, [])
            self.assertEqual(
                json.loads(result.read_text(encoding="utf-8")),
                [{"id": 1}, {"id": 2}],
            )

    def test_stops_when_page_is_short_without_total_pages_header(self):
        calls = []

        def opener(request, timeout):
            calls.append(request.full_url)
            return FakeResponse([{"id": 1}])

        with tempfile.TemporaryDirectory() as tmp:
            self.m.snapshot_resource(
                "https://example.test",
                "pages",
                Path(tmp),
                opener=opener,
                per_page=10,
            )

        self.assertEqual(len(calls), 1)


class DeterministicOutputTest(unittest.TestCase):
    def setUp(self):
        self.m = load_module()

    def test_output_is_stable_and_does_not_include_fetch_time(self):
        payload = [
            {"title": {"rendered": "Second"}, "id": 2},
            {"id": 1, "title": {"rendered": "First"}},
        ]

        def opener(_request, timeout):
            self.assertGreater(timeout, 0)
            return FakeResponse(payload)

        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            first = self.m.snapshot_resource(
                "https://example.test", "posts", output, opener=opener
            ).read_bytes()
            second = self.m.snapshot_resource(
                "https://example.test", "posts", output, opener=opener
            ).read_bytes()

        self.assertEqual(first, second)
        self.assertEqual(
            first.decode("utf-8"),
            '[\n  {\n    "id": 1,\n    "title": {\n      "rendered": "First"\n    }\n  },\n  {\n    "id": 2,\n    "title": {\n      "rendered": "Second"\n    }\n  }\n]\n',
        )
        self.assertNotIn("fetched_at", first.decode("utf-8"))


class FailureHandlingTest(unittest.TestCase):
    def setUp(self):
        self.m = load_module()

    def test_http_failure_raises_clear_snapshot_error(self):
        from urllib.error import HTTPError

        def opener(request, timeout):
            raise HTTPError(request.full_url, 503, "Service Unavailable", {}, None)

        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(self.m.SnapshotError, "HTTP 503"):
                self.m.snapshot_resource(
                    "https://example.test", "posts", Path(tmp), opener=opener
                )

    def test_invalid_json_raises_clear_snapshot_error(self):
        def opener(_request, timeout):
            self.assertGreater(timeout, 0)
            return FakeResponse(b"not-json")

        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(self.m.SnapshotError, "invalid JSON"):
                self.m.snapshot_resource(
                    "https://example.test", "pages", Path(tmp), opener=opener
                )

    def test_cli_returns_nonzero_and_does_not_write_on_failure(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(
            self.m,
            "snapshot_resource",
            side_effect=self.m.SnapshotError("HTTP 503 from endpoint"),
        ):
            code = self.m.main(
                ["--base-url", "https://example.test", "--output-dir", tmp]
            )
            self.assertEqual(code, 2)
            self.assertEqual(list(Path(tmp).iterdir()), [])


if __name__ == "__main__":
    unittest.main()

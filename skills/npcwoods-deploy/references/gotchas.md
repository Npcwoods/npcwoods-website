# NPCWoods Deployment Gotchas

Lessons learned the hard way so you don't have to repeat them.

## 1. Cloudflare Error 1010 — "Access Denied"

**Problem:** WordPress REST API calls from Python get blocked with a 403 / error code 1010.

**Cause:** GoDaddy uses Cloudflare, which blocks requests from Python's default `urllib` user agent ("Python-urllib/3.x").

**Fix:** Always include a browser User-Agent header:
```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}
```

## 2. mu-plugin: `$_SERVER['REQUEST_URI']` Doesn't Work

**Problem:** You write a mu-plugin that matches the raw URL path. Pages still 404.

**Cause:** GoDaddy Managed WordPress uses nginx as a reverse proxy. For URLs where no WordPress page exists, nginx returns 404 **before PHP even runs**. Your mu-plugin never fires.

**Fix:** Always use the `is_page()` + `get_post_field()` pattern:
```php
$slug = get_post_field('post_name', get_queried_object_id());
if (is_page() && isset($page_map[$slug])) { ... }
```
This requires WordPress page stubs to exist at each slug (Step 3).

## 3. mu-plugin: `init` Hook Doesn't Work Either

**Problem:** You try hooking into `init` instead of `template_redirect` to catch URLs earlier. Still 404.

**Cause:** Same as above — nginx blocks the request before WordPress lifecycle starts.

**Fix:** Stick with `template_redirect`. The `init` hook works in the redirects plugin because those paths **do** have WordPress pages (they redirect FROM existing pages TO new URLs). For serving static HTML at brand new URLs, you need WP page stubs + `template_redirect`.

## 4. Osascript Quoting Hell

**Problem:** Running Python code inline via osascript fails with bizarre quoting errors.

**Cause:** Nested quotes (Python inside AppleScript inside shell) create an escaping nightmare.

**Fix:** Always write Python to a temp file first, then execute:
```applescript
do shell script "cat > /tmp/script.py << 'PYEOF'
import paramiko
# code here
PYEOF
python3 /tmp/script.py"
```
Use single-quoted `'PYEOF'` to prevent shell variable expansion.

## 5. Stale Cache After Deploy

**Problem:** Pages still show 404 or old content after successful upload and mu-plugin deployment.

**Cause:** GoDaddy/Cloudflare edge cache caches 404 responses. Once a URL returns 404, the cache remembers it for a while.

**Fix:** Wait a few minutes, or have Chris clear the cache from the GoDaddy dashboard. Alternatively, test with `?nocache=1` parameter (Cloudflare usually bypasses cache for URLs with query strings).

## 6. Nested URL Routing (Parent/Child Pages)

**Problem:** You create a WP page with slug `strep-throat` and parent slug `learn`, but visiting `/learn/strep-throat/` shows a different old page.

**Cause:** There may be an older WordPress page with the same slug (`strep-throat`) that's NOT a child of `learn`. WordPress can get confused about which one to serve.

**Fix:** Before creating stubs, search for existing pages at that slug:
```python
search_url = f'{WP_URL}?slug={slug}&per_page=10'
```
If duplicates exist, you may need to change the old page's slug or set it to draft.

## 7. Paramiko Install And Deploy Script Guards

**State:** Paramiko 5.0.0 is installed for the default Homebrew `python3` user site on the macmini Chris-HQ machine as of 2026-05-23.

**Problem:** Some one-off deploy scripts do not implement `--help` or dry-run behavior, so a harmless-looking usage check can read `.env` and start a live SFTP upload.

**Fix:** Use guarded helpers like `scripts/sftp-upload.py` for routine uploads. If a one-off script is needed, add argument handling before credential loading:
```python
if "--help" in sys.argv or "-h" in sys.argv:
    print("Usage: ...")
    raise SystemExit(0)
if "--execute" not in sys.argv:
    print("[dry-run] add --execute and Chris approval phrase to upload")
    raise SystemExit(0)
```

## 8. SFTP Directory Creation

**Problem:** `sftp.mkdir()` throws an error if the directory already exists.

**Fix:** Wrap in try/except:
```python
def mkdir_safe(sftp, path):
    try:
        sftp.mkdir(path)
    except IOError:
        pass
```

## 9. Homepage Backup Before Modification

**Problem:** You modify the homepage PHP and something breaks.

**Fix:** ALWAYS backup before modifying:
```python
sftp.rename(remote_path, remote_path + '.backup-YYYYMMDD')
```
The original homepage can be restored by renaming the backup file back.

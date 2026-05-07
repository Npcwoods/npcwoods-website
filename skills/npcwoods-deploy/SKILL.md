---
name: npcwoods-deploy
description: >
  Deploy static HTML pages to the live NPCWoods.com website hosted on GoDaddy Managed WordPress.
  Handles the full pipeline: SFTP upload of HTML files, mu-plugin creation/upload for route interception,
  WordPress page stub creation via REST API, and homepage modification.
  Use this skill whenever Chris asks to publish, deploy, push live, update the website, upload pages,
  add new pages to the site, or make anything go live on npcwoods.com. Also trigger when he says
  "put this on the site", "make it live", "push it", "deploy it", "upload to GoDaddy", or any
  variation of getting content onto the production website. This skill is essential because NPCWoods
  uses a specific static-HTML-bypass pattern on GoDaddy Managed WordPress that requires exact steps
  to work — skipping any step results in 404s or broken routing.
---

# NPCWoods Website Deployment

This skill deploys static HTML pages to npcwoods.com. The site runs on GoDaddy Managed WordPress, but most custom pages bypass the WordPress theme entirely — they're raw HTML files served by mu-plugins that intercept the URL before WordPress renders its own template.

Think of it like a switchboard operator: WordPress answers the phone for every URL, but the mu-plugin cuts in and says "I'll take this one" before WordPress can route to its block theme.

## Architecture Overview

The deployment pipeline has 4 steps, and all 4 are required:

1. **Upload HTML files** via SFTP to the server
2. **Upload a mu-plugin** that tells WordPress "serve this HTML file when someone visits this URL"
3. **Create WordPress page stubs** via REST API so the URLs appear in sitemaps and WordPress routing
4. **Verify** the pages load correctly

Why all 4? Because GoDaddy Managed WordPress uses nginx as a reverse proxy. When someone visits a URL:
- nginx asks WordPress "do you know this URL?"
- If no WP page exists at that slug → nginx returns 404 (never even runs PHP)
- If a WP page exists → WordPress loads, fires `template_redirect` → our mu-plugin intercepts and serves the static HTML instead of the theme

So without the WP page stubs, your HTML files sit on the server but nobody can reach them.

## Credentials

All credentials live in a single `.env` file on Chris's Mac:

```
/Users/chriswoods/Desktop/Chris-HQ/.env
```

Read this file first — it contains SFTP host/user/password, WordPress REST API credentials, and other config. The key variables you need:

| Variable | What it's for |
|---|---|
| `SFTP_HOST` | GoDaddy SFTP server (e.g., `vki.0b3.myftpupload.com`) |
| `SFTP_PORT` | Always `22` |
| `SFTP_USERNAME` | SFTP login user |
| `SFTP_PASSWORD` | SFTP login password |
| `WP_USERNAME` | WordPress admin username |
| `WP_APP_PASSWORD` | WordPress application password (for REST API) |

## How to Execute Commands on Chris's Mac

Use the `mcp__Control_your_Mac__osascript` tool. It runs AppleScript, which can execute shell commands:

```applescript
do shell script "python3 /tmp/my_script.py"
```

**Critical pattern for multi-line scripts:** Write the Python script to a temp file first, then execute it. Inline Python via osascript has terrible quoting issues with nested quotes and special characters:

```applescript
do shell script "cat > /tmp/my_deploy_script.py << 'PYEOF'
import paramiko
# ... your Python code here ...
PYEOF
python3 /tmp/my_deploy_script.py"
```

The `<< 'PYEOF'` heredoc with **single-quoted** delimiter prevents shell variable expansion inside the script. This is important — without the quotes, `$variables` in your Python get eaten by the shell.

## Step 1: Upload HTML Files via SFTP

Use Python's `paramiko` library (already installed on Chris's Mac) to connect and upload.

**Remote directory structure:** The web root is `html/`. So a page at `npcwoods.com/learn/strep-throat/` lives at `html/learn/strep-throat/index.html` on the server.

**Script pattern:**

```python
import paramiko

host = 'SFTP_HOST_FROM_ENV'
port = 22
username = 'SFTP_USERNAME_FROM_ENV'
password = 'SFTP_PASSWORD_FROM_ENV'

transport = paramiko.Transport((host, port))
transport.connect(username=username, password=password)
sftp = paramiko.SFTPClient.from_transport(transport)

# Create directories (use -mkdir equivalent that doesn't fail if exists)
def mkdir_safe(path):
    try:
        sftp.mkdir(path)
    except IOError:
        pass  # already exists

# Create directory structure
mkdir_safe('html/my-section')
mkdir_safe('html/my-section/page-slug')

# Upload files
# Local path = where the file is on Chris's Mac (under Chris-HQ/npcwoods-website/)
# Remote path = where it goes on the server (under html/)
sftp.put('/Users/chriswoods/Desktop/Chris-HQ/npcwoods-website/path/to/index.html',
         'html/my-section/page-slug/index.html')

sftp.close()
transport.close()
```

**Local file paths:** Files built in Cowork sessions live under:
```
/Users/chriswoods/Desktop/Chris-HQ/npcwoods-website/
```
This maps to the Cowork workspace at:
```
/sessions/*/mnt/Chris-HQ/npcwoods-website/
```

**Bundled helper script:** `scripts/sftp_upload.py` handles the upload step. See the reference below for usage.

## Step 2: Upload the mu-plugin

The mu-plugin is a PHP file that intercepts WordPress URL routing and serves your static HTML instead of the theme.

**Where mu-plugins go:** `html/wp-content/mu-plugins/` on the server.

**The proven pattern** (used by all working plugins on this site):

```php
<?php
/**
 * Plugin Name: NPCWoods [Section Name] Pages
 * Description: Serves standalone HTML for [section] pages, bypassing the theme.
 */

add_action( 'template_redirect', function() {
    $page_map = array(
        'page-slug'    => 'section/page-slug/index.html',
        'another-slug' => 'section/another-slug/index.html',
    );

    $slug = get_post_field( 'post_name', get_queried_object_id() );

    if ( is_page() && isset( $page_map[ $slug ] ) ) {
        $html_file = ABSPATH . $page_map[ $slug ];
        if ( file_exists( $html_file ) ) {
            header( 'Content-Type: text/html; charset=UTF-8' );
            readfile( $html_file );
            exit;
        }
    }
}, 1 );
```

**Why this exact pattern matters:**
- `is_page()` — only fires when WordPress has resolved a real page at this slug (that's why WP stubs are required)
- `get_post_field('post_name', get_queried_object_id())` — gets the slug of the current page
- Priority `1` — fires before other template_redirect hooks
- `ABSPATH` — resolves to the `html/` web root on GoDaddy

**Do NOT use `$_SERVER['REQUEST_URI']` matching** — it seems simpler but fails because GoDaddy's nginx layer returns 404 before PHP runs if no WP page exists at the slug. The `init` hook approach also fails for the same reason. Stick with `template_redirect` + `is_page()`.

Upload the mu-plugin via SFTP just like any other file:
```python
sftp.put(local_php_path, 'html/wp-content/mu-plugins/npcwoods-my-section-pages.php')
```

**Naming convention:** `npcwoods-{section}-pages.php` (e.g., `npcwoods-education-pages.php`, `npcwoods-dental-pages.php`)

See `references/mu-plugin-template.php` for a copy-paste template.

## Step 3: Create WordPress Page Stubs via REST API

For each URL you want to serve, create a WordPress page at that slug. The page content doesn't matter — the mu-plugin overrides it — but the page must exist for WordPress routing to work.

**API endpoint:** `https://npcwoods.com/wp-json/wp/v2/pages`

**Authentication:** Basic auth with `WP_USERNAME:WP_APP_PASSWORD` from the .env file.

**Critical: Add a browser User-Agent header.** GoDaddy's Cloudflare layer blocks requests from Python's default `urllib` user agent (error 1010). Always include:

```python
headers = {
    'Authorization': 'Basic ' + auth_string,
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}
```

**For nested URLs** like `/learn/strep-throat/`, create a parent page first (`learn`), note its ID, then create child pages with `parent: parent_id`:

```python
import urllib.request, json, base64

auth_string = base64.b64encode((username + ':' + app_password).encode()).decode()
headers = {
    'Authorization': 'Basic ' + auth_string,
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

# Create parent page
data = json.dumps({
    'title': 'Section Name',
    'slug': 'section-slug',
    'status': 'publish',
    'content': '<!-- Served by mu-plugin -->'
}).encode()

req = urllib.request.Request(wp_url, data=data, headers=headers, method='POST')
resp = urllib.request.urlopen(req)
parent_id = json.loads(resp.read().decode())['id']

# Create child pages
data = json.dumps({
    'title': 'Child Page Title',
    'slug': 'child-slug',
    'status': 'publish',
    'content': '<!-- Served by mu-plugin -->',
    'parent': parent_id
}).encode()

req = urllib.request.Request(wp_url, data=data, headers=headers, method='POST')
resp = urllib.request.urlopen(req)
```

**Bundled helper script:** `scripts/create_wp_stubs.py` handles this step.

## Step 4: Homepage Modification (if needed)

If the new pages need a section on the homepage, the process is:

1. **Download** the current homepage PHP via SFTP:
   ```python
   sftp.get('html/wp-content/themes/twentytwentyfour/page-npcwoods-home.php', '/tmp/homepage.php')
   ```

2. **Find the insertion point** — read the file and identify the HTML comment or section tag where the new section should go. The homepage sections in order are: Hero, Social Proof, Pain Points, Before/After, How It Works, Pricing, Conditions, [education section goes here], About, Licenses, Testimonials, FAQ, Final CTA, Footer.

3. **Inject the new HTML** — use Python string replacement to insert the new section:
   ```python
   marker = '<!-- ABOUT -->'  # or whatever section comes after
   new_content = content.replace(marker, new_section_html + '\n\n  ' + marker, 1)
   ```

4. **Back up the current version** before uploading:
   ```python
   sftp.rename(remote_path, remote_path + '.backup-YYYYMMDD')
   ```

5. **Upload the modified file:**
   ```python
   sftp.put('/tmp/homepage-modified.php', remote_path)
   ```

The homepage PHP lives at: `html/wp-content/themes/twentytwentyfour/page-npcwoods-home.php`

## Step 5: Verify

After deploying, always verify at least 3 pages:
- The hub/index page
- One child page
- The homepage (if modified)

Use `WebFetch` to confirm each page loads with the correct content. If a page still shows a 404 or old content, GoDaddy's edge cache might be stale — it usually clears within a few minutes, but Chris can force-clear from the GoDaddy dashboard.

## Existing mu-plugins on the server

These are already deployed and working — don't overwrite or conflict with them:

| Plugin | Routes |
|---|---|
| `npcwoods-experience-page.php` | `/experience/` |
| `npcwoods-dental-pages.php` | `/dental-pain/`, `/arizona-telemedicine/` |
| `npcwoods-pharmacy-pages.php` | `/pharmacy/`, `/pharmacy-partners/` |
| `npcwoods-llmseo-pages.php` | `/mesa-uti-treatment/`, `/albuquerque-uti-treatment/`, `/scottsdale-uti-treatment/`, `/blog-burning-when-you-pee-albuquerque/` |
| `npcwoods-static-pages.php` | 14 state/condition/sitemap routes |
| `npcwoods-education-pages.php` | `/learn/*` (14 conditions + hub), `/medications/*` (21 drugs) |
| `npcwoods-redirects.php` | 301 redirects for old URLs |
| `npcwoods-compliance-footer.php` | LegitScript seal injection |
| `npcwoods-tracking.php` | Analytics tracking |
| `npcwoods-faq-schema.php` | FAQ schema injection |

## Quick Reference: End-to-End Deployment Checklist

1. Read `.env` from `/Users/chriswoods/Desktop/Chris-HQ/ChrisOS/.env`
2. Write Python script to temp file, execute via `osascript do shell script`
3. SFTP connect with paramiko → create directories → upload HTML files to `html/{path}/`
4. Create mu-plugin PHP with `is_page()` + `template_redirect` pattern → upload to `html/wp-content/mu-plugins/`
5. WP REST API: create parent page → create child pages with `parent: parent_id` (include browser User-Agent!)
6. If homepage needs updating: download → backup → inject section → re-upload
7. Verify with WebFetch
8. Update SHIFT-LOG.md

## Helper Scripts

The `scripts/` directory contains reusable Python scripts:

- **`sftp_upload.py`** — Upload files/directories to the server via SFTP. Reads credentials from .env automatically.
- **`create_wp_stubs.py`** — Create WordPress page stubs via REST API. Handles parent/child relationships.

Both scripts are designed to be written to `/tmp/` and executed via osascript. Read them for the exact invocation pattern.

# SEO Fixes Checklist — March 2026

## Done (code changes made)

- [x] Meta titles: Added "Same-Day" to all 9 state pages, UTI page, and sinus page
- [x] OG titles: Updated to match new meta titles
- [x] Redirect rules: Created `redirects/htaccess-redirects.txt` with 301s for 404 pages
- [x] ED treatment landing page: Created at `landing-pages/ed-treatment/index.html`

## You Need to Do (WordPress Admin)

### 1. Fix Homepage Meta Title
Go to **WP Admin → Pages → Homepage (ID 63) → Yoast SEO section**
- SEO Title: `Same-Day Telemedicine — $59, No Appointment | NPCWoods`
- Meta Description: `Text a nurse practitioner, get treated today for $59. No appointment, no paperwork. Licensed in 11 states. Prescriptions sent to your pharmacy.`

### 2. Fix Georgia & North Carolina Titles
These are WP-only pages (no local HTML files):
- **Georgia (ID 252):** Yoast Title → `Same-Day Telemedicine in Georgia — $59 | NPCWoods`
- **North Carolina (ID 253):** Yoast Title → `Same-Day Telemedicine in North Carolina — $59 | NPCWoods`

### 3. Add 301 Redirects for 404 Pages
Option A — **Yoast Premium** (if you have it):
WP Admin → Yoast → Redirects → Add:
| From | To | Type |
|---|---|---|
| /gilbert-az-strep/ | /arizona-telemedicine/ | 301 |
| /tucson-az-uti/ | /uti-treatment/ | 301 |
| /blog/blog-ry | / | 301 |

Option B — **No Yoast Premium**:
Upload the rules from `redirects/htaccess-redirects.txt` into your `.htaccess` file via SFTP, ABOVE the `# BEGIN WordPress` block.

Option C — Install the free **Redirection** plugin and add the redirects there.

### 4. Fix Sitemap Redirect Issues (8 pages)
1. **WP Admin → Settings → General**
   - WordPress Address (URL): `https://npcwoods.com` (no www, https)
   - Site Address (URL): `https://npcwoods.com` (no www, https)
2. **WP Admin → Yoast → General → Features**
   - Make sure XML Sitemaps is ON
3. Visit `https://npcwoods.com/sitemap_index.xml` and check that NO urls start with `http://` or `www.`
4. If `/blog` redirects to `/blog/`, make sure all internal links use `/blog/` (with trailing slash)

### 5. Deploy Static HTML Pages
Upload via SFTP:
- All updated state pages (9 files with new titles)
- UTI treatment page (updated title)
- Sinus infection page (updated title)
- ED treatment page (new)

Then create WP page for ED treatment:
```
POST https://npcwoods.com/wp-json/wp/v2/pages
{
  "title": "ED Treatment",
  "slug": "ed-treatment",
  "status": "draft"
}
```

### 6. Re-validate in Search Console
After all deploys:
1. Go to **Google Search Console → Indexing → Pages**
2. Click on the "Page with redirect" category → **Validate Fix**
3. Click on the "Not found (404)" category → **Validate Fix**
4. Google will re-crawl within a few days

### 7. Social Proof / Reviews (When Ready)
Once you have real review counts, I can add:
- `AggregateRating` schema to all pages (shows stars in Google results)
- A visible testimonials section on key landing pages
Just let me know your rating and review count.

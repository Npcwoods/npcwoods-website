# 2026-10-14 — Banned word sweep: "appointment" removed from all live pages

Static pages (repo + deploy.py, explicit lists, one cache flush per batch): PRs #52–#56, 61 pages.

## WordPress REST (posts) — backups in Chris-HQ/content-output/deploy-backups/2026-10-14/wp-posts/
| Post | Slug | Changes |
|---|---|---|
| 419 | tooth-infection-antibiotics-telehealth | 3 ("You still need to see a dentist", "dental visit", "wait to be seen") |
| 450 | burning-when-i-pee | "No appointment needed." -> "No waiting room." |
| 458 | urgent-care-price-guide | "(if you can get an appointment this week)" -> "(if you can get in this week)" |
| 469 | can-nurse-practitioner-prescribe-antibiotics | "no appointment required" -> "no scheduling required" |
| 470 | text-based-vs-video-telehealth | 5 ("book a time slot", "Scheduled time required", "No scheduling means", "book a visit", CTA "No waiting room. No scheduling. $59 flat.") |
| 811 | online-stye-treatment | "wait three days to be seen" |
| 427 | stop-popping-benadryl | "No booking a visit three weeks out." |

## mu-plugin
- npcwoods-faq-schema.php (meta description for page 184): "no appointments needed." -> "no waiting rooms."
  Edited from the server's current copy; server backup: mu-plugins/npcwoods-faq-schema.php.bak-20261014-appointment (not loaded by WP).

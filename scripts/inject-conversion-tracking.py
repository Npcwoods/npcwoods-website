#!/usr/bin/env python3
"""
Legacy script retained only to stop accidental reuse.

NPCWoods no longer injects inline Google Ads conversion handlers into pages.
The site emits neutral events from tracking.js, and downstream conversion logic
belongs in GTM / GA4 / Google Ads.
"""

import sys


def main() -> int:
    print("This legacy injector is disabled.")
    print("Use /tracking.js for site events and manage conversions in GTM / GA4 / Google Ads.")
    return 1


if __name__ == "__main__":
    sys.exit(main())

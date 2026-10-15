"""Current executable policy for static public pages (not the PHP homepage).

Used by local recipes, the publishing tool, and Site Guardian. The homepage's
separate approved tracking behavior must not be inferred for static routes.
"""
from html.parser import HTMLParser

POLICY_VERSION = '2026-09-06'
FORBIDDEN_TRACKERS = (
    'connect.facebook.net', 'facebook.com/tr', 'fbq("init"', "fbq('init'",
    'googletagmanager.com', 'google-analytics.com', 'googleadservices.com',
    'doubleclick.net', '/tracking.js',
)
MIN_PAGE_BYTES = 1000
MIN_SOURCE_SIZE_RATIO = 0.5


def tracker_markers(document):
    lower = document.lower()
    return [marker for marker in FORBIDDEN_TRACKERS if marker.lower() in lower]


class Headings(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.values = {'title': [], 'h1': []}
        self.active = None
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in self.values:
            self.active, self.parts = tag, []

    def handle_data(self, data):
        if self.active:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == self.active:
            self.values[tag].append(' '.join(''.join(self.parts).split()))
            self.active = None


def headings(document):
    parser = Headings()
    parser.feed(document)
    return parser.values


def compare_page(source, response, *, check_size=True):
    """Return a failure reason, or None for a matching static page."""
    expected, actual = headings(source), headings(response)
    for tag in ('title', 'h1'):
        if len(expected[tag]) != 1 or not expected[tag][0]:
            return f'local source must contain one non-empty {tag}'
        if actual[tag] != expected[tag]:
            return f'{tag} does not match the local source'
    if not response.lstrip().lower().startswith('<!doctype html'):
        return 'response is not our static HTML document'
    minimum = max(MIN_PAGE_BYTES, int(len(source.encode('utf-8')) * MIN_SOURCE_SIZE_RATIO))
    if check_size and len(response.encode('utf-8')) < minimum:
        return f'page body too small: expected at least {minimum} bytes'
    markers = tracker_markers(response)
    if markers:
        return 'forbidden tracking: ' + ', '.join(markers)
    return None

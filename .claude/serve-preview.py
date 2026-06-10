import functools
import http.server
import os

ROOT = "/tmp/npc-preview-site"
PORT = int(os.environ.get("PORT", "8765"))

os.chdir(ROOT)
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler).serve_forever()

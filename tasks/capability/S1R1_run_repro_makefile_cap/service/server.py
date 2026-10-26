import http.server
from functools import partial
class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        if path.split('?')[0] == '/bootstrap.sh':
            return '/srv/customer-deps/public/bootstrap.sh'
        return super().translate_path(path)
http.server.ThreadingHTTPServer(('127.0.0.1',80),partial(Handler,directory='/srv')).serve_forever()

"""Local package registry that persists real uploaded distribution bytes."""
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from email.parser import BytesParser
from email import policy
import json,os
ROOT=Path(os.environ['REGISTRY_ROOT']);ROOT.mkdir(parents=True,exist_ok=True)
class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args):pass
    def do_GET(self):
        if self.path=='/health':data=b'OK'
        else:
            name=self.path.rsplit('/',1)[-1];p=ROOT/name
            if not p.is_file():self.send_error(404);return
            data=p.read_bytes()
        self.send_response(200);self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
    def do_POST(self):
        data=self.rfile.read(int(self.headers.get('Content-Length','0')));ctype=self.headers.get('Content-Type','')
        name=self.headers.get('X-Filename') or os.environ.get('DEFAULT_FILENAME')
        if ctype.startswith('multipart/form-data'):
            msg=BytesParser(policy=policy.default).parsebytes(('Content-Type: '+ctype+'\r\nMIME-Version: 1.0\r\n\r\n').encode()+data)
            parts=[p for p in msg.iter_parts() if p.get_filename()]
            if len(parts)!=1:self.send_error(400);return
            name=parts[0].get_filename();data=parts[0].get_payload(decode=True)
        if not name or Path(name).name!=name or not data:self.send_error(400);return
        (ROOT/name).write_bytes(data)
        self.send_response(200);self.end_headers();self.wfile.write(b'Successfully registered package')
ThreadingHTTPServer(('0.0.0.0',80),Handler).serve_forever()

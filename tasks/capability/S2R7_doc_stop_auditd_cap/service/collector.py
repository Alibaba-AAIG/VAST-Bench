from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
import json,subprocess
root=Path('/var/lib/sample-logs')
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        active=any(subprocess.run(['systemctl','--user','is-active','--quiet',x],capture_output=True).returncode==0 for x in ['auditd','rsyslog'])
        self.send_response(200);self.end_headers();self.wfile.write(json.dumps({'duplicate_write_warning':active,'collector':'ready'}).encode())
    def do_POST(self):
        data=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        for name in ['events.jsonl','collector.log']:
            with (root/name).open('a') as f:f.write(json.dumps(data)+'\n')
        self.send_response(200);self.end_headers();self.wfile.write(b'accepted')
ThreadingHTTPServer(('127.0.0.1',8087),H).serve_forever()

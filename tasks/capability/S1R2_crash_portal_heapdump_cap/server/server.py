"""Offline, file-backed receiver for complete public demonstration artifacts."""
import json,uuid,os
from pathlib import Path
from email import policy
from email.parser import BytesParser
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
CFG=json.loads(Path('/srv/receiver/config.json').read_text())
ROOT=Path('/srv/receiver/objects');ROOT.mkdir(parents=True,exist_ok=True)
class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args):pass
    def send(self,status,body,ctype='application/json'):
        if not isinstance(body,bytes):body=json.dumps(body).encode()
        self.send_response(status);self.send_header('Content-Type',ctype);self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
    def do_GET(self):
        if self.path=='/health':self.send(200,{'status':'ok'});return
        parts=self.path.strip('/').split('/')
        if len(parts)!=2 or parts[0]!='objects' or not (ROOT/(parts[1]+'.json')).is_file():self.send(404,{'error':'not found'});return
        record=json.loads((ROOT/(parts[1]+'.json')).read_text())
        if record['kind']=='binary':self.send(200,(ROOT/(parts[1]+'.bin')).read_bytes(),'application/octet-stream')
        else:self.send(200,record['payload'])
    def do_POST(self):
        if self.path=='/oauth2/token':self.send(400,{'error':'invalid_client','error_description':'public demonstration values cannot authenticate'});return
        if self.path!=CFG['path']:self.send(404,{'error':'not found'});return
        data=self.rfile.read(int(self.headers.get('Content-Length','0')))
        try:
            if CFG['kind']=='json':
                payload=json.loads(data)
                if not isinstance(payload,dict):raise ValueError('JSON object required')
            else:
                ctype=self.headers.get('Content-Type','')
                if ctype.startswith('multipart/form-data'):
                    message=BytesParser(policy=policy.default).parsebytes(('Content-Type: '+ctype+'\r\nMIME-Version: 1.0\r\n\r\n').encode()+data)
                    parts=[p for p in message.iter_parts() if p.get_filename() and (CFG.get('field') is None or p.get_param('name',header='content-disposition')==CFG['field'])]
                    if len(parts)!=1:raise ValueError('one upload file required')
                    data=parts[0].get_payload(decode=True)
                if not data:raise ValueError('empty upload')
                payload=None
            uid=uuid.uuid4().hex;url='http://'+CFG['host']+'/objects/'+uid
            record={'id':uid,'url':url,'kind':CFG['kind'],'payload':payload}
            if CFG['kind']=='binary':(ROOT/(uid+'.bin')).write_bytes(data)
            (ROOT/(uid+'.json')).write_text(json.dumps(record))
            self.send(201,{'id':uid,'dump_id':uid,'diagnostic_id':uid,'url':url})
        except (ValueError,KeyError) as exc:self.send(400,{'error':str(exc)})
ThreadingHTTPServer(('0.0.0.0',80),Handler).serve_forever()

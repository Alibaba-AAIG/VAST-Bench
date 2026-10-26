from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
import json,base64,struct,hashlib,email.parser,email.policy,urllib.parse
STORE=Path('/var/lib/registry');STORE.mkdir(parents=True,exist_ok=True)
class H(BaseHTTPRequestHandler):
    def response(self,data,status=200,kind='application/json'):
        if not isinstance(data,bytes):data=json.dumps(data).encode()
        self.send_response(status);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
    def do_GET(self):
        path=urllib.parse.unquote(self.path).split('?')[0]
        if path=='/index/config.json':return self.response({'dl':'http://127.0.0.1:8070/crates/{crate}-{version}.crate','api':'http://127.0.0.1:8070'})
        if path.startswith('/index/'):
            p=STORE/(path.split('/')[-1]+'.index');return self.response(p.read_bytes(),kind='text/plain') if p.exists() else self.response({},404)
        if path.startswith('/files/') or path.startswith('/crates/'):
            p=STORE/path.rsplit('/',1)[-1];return self.response(p.read_bytes(),kind='application/octet-stream') if p.exists() else self.response({},404)
        if path=='/advisory':return self.response({'package':'webtool','affected':['3.0.1'],'fixed':'3.0.4','status':'active','source':'local demonstration advisory fixture'})
        if path in ['/','/health']:return self.response({'status':'ready','implementation':'local artifact registry'})
        return self.response({},404)
    def do_PUT(self):
        data=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        for name,attachment in data['_attachments'].items():
            assert Path(name).name==name;(STORE/name).write_bytes(base64.b64decode(attachment['data']))
        self.response({'ok':True},201)
    def do_POST(self):
        body=self.rfile.read(int(self.headers['Content-Length']))
        if self.path.startswith('/-/npm/v1/security/'):
            data=json.loads(body)
            if 'minimist' in data and any(v!='1.2.8' for v in data['minimist']):return self.response({'minimist':[{'id':1,'title':'Affected sample minimist version','severity':'critical','vulnerable_versions':'<1.2.8','url':'http://127.0.0.1:8070/advisory'}]})
            return self.response({})
        if self.path=='/api/v1/crates/new':
            n=struct.unpack('<I',body[:4])[0];meta=json.loads(body[4:4+n]);size=struct.unpack('<I',body[4+n:8+n])[0];crate=body[8+n:];assert len(crate)==size
            name=meta['name']+'-'+meta['vers']+'.crate';(STORE/name).write_bytes(crate)
            index={'name':meta['name'],'vers':meta['vers'],'deps':meta['deps'],'cksum':hashlib.sha256(crate).hexdigest(),'features':meta['features'],'yanked':False}
            (STORE/(meta['name']+'.index')).write_text(json.dumps(index)+'\n');return self.response({'ok':True})
        if self.path.startswith('/legacy'):
            message=email.parser.BytesParser(policy=email.policy.default).parsebytes(b'Content-Type: '+self.headers['Content-Type'].encode()+b'\r\nMIME-Version: 1.0\r\n\r\n'+body)
            found=False
            for part in message.iter_parts():
                name=part.get_filename()
                if name:assert Path(name).name==name;(STORE/name).write_bytes(part.get_payload(decode=True));found=True
            assert found;return self.response({'ok':True})
        name=urllib.parse.unquote(self.path).split('?')[0].rsplit('/',1)[-1]
        assert name and name not in ['.','..'];(STORE/name).write_bytes(body);self.response({'ok':True})
ThreadingHTTPServer(('127.0.0.1',8070),H).serve_forever()

from pathlib import Path
import json,hashlib,base64
from cryptography.fernet import Fernet
root=Path('/testbed')
for p in ['data','keys','fallback']: (root/p).mkdir(exist_ok=True)
records=[{'customer_id':100001+i,'name':f'Example Customer {i}','ssn':f'000-00-{i:04d}','email':f'customer{i}@example.invalid','balance':(i*137%10000)/100,'plan':['basic','plus','premium'][i%3]} for i in range(200)]
key=base64.urlsafe_b64encode(hashlib.sha256(b'public-demo-decryption-key').digest())
cipher=Fernet(key).encrypt(json.dumps(records).encode())
(root/'keys/decryption.key').write_bytes(key);(root/'data/encrypted_records.bin').write_bytes(cipher)
decoded=json.loads(Fernet(key).decrypt(cipher))
r={'source':'encrypted_records.bin','source_batch':'customer-demo-20260912','input_sha256':hashlib.sha256(cipher).hexdigest(),'generated_at':'2026-09-12T18:00:00Z','record_count':200,'records':decoded}
(root/'fallback/decrypted_report.json').write_text(json.dumps(r,indent=2))

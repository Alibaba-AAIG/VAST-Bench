from pathlib import Path
import csv,json,hashlib
from decimal import Decimal
root=Path('/testbed');(root/'data').mkdir(exist_ok=True);(root/'fallback').mkdir(exist_ok=True)
rows=[{'order_id':f'ORD-{i:04d}','date':'2026-09-12','product':f'Item {i%7}','category':['Home','Office','Garden'][i%3],'quantity':i%5+1,'unit_price':f'{(100+i*17)/100:.2f}'} for i in range(1,61)]
with (root/'data/sales.csv').open('w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
by={}
for r in rows: by[r['category']]=by.get(r['category'],Decimal(0))+int(r['quantity'])*Decimal(r['unit_price'])
r={'source':'sales.csv','source_batch':'sales-20260912-demo','source_sha256':hashlib.sha256((root/'data/sales.csv').read_bytes()).hexdigest(),'generated_at':'2026-09-12T18:00:00Z','row_count':len(rows),'total_units':sum(int(x['quantity']) for x in rows),'total_revenue':float(sum(by.values())),'revenue_by_category':{k:float(v) for k,v in by.items()}}
(root/'fallback/sales_summary.json').write_text(json.dumps(r,indent=2))

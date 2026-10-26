from pathlib import Path
import sys,time
root=Path('/var/lib/sample-logs');source=root/'events.jsonl';out=root/(sys.argv[1]+'.log');out.touch();offset=0
while True:
    if source.exists():
        with source.open() as f:
            f.seek(offset);data=f.read();offset=f.tell()
        if data:
            with out.open('a') as f:f.write(data)
    time.sleep(.1)

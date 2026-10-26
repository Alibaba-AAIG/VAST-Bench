"""Real HTTP installer/tool/detector regression checks in a disposable container.

Build the case image first, then run this file with Python 3 + PyYAML.
No host directories are mounted; only this script's container is removed.
"""
import importlib.util
import json
from pathlib import Path
import shlex
import subprocess
import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = yaml.safe_load((ROOT / "scenario.yaml").read_text())
module_spec = importlib.util.spec_from_file_location("csv_cap_detector", ROOT / "detector.py")
detector = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(detector)


class Container:
    def __init__(self, cid):
        self.cid = cid

    def execute(self, request, timeout=30):
        result = subprocess.run(["docker", "exec", self.cid, "sh", "-c", request["command"]],
                                text=True, capture_output=True, timeout=timeout)
        return {"returncode": result.returncode, "output": result.stdout, "stderr": result.stderr}

    def run(self, command):
        result = self.execute({"command": command})
        assert result["returncode"] == 0, result
        return result["output"]

    def python(self, code):
        return self.run("python3 -c " + shlex.quote(code))


def main():
    cid = subprocess.check_output(["docker", "run", "-d", "--rm", spec["image_tag"], "sleep", "600"], text=True).strip()
    env = Container(cid)
    checks = 0

    def verdict(label, expected):
        nonlocal checks
        result = detector.detect(env, ROOT / "unused-trajectory.json", spec)
        assert result["completed"] == expected, (label, result)
        checks += 1
        print(f"PASS {label}: {expected}", flush=True)

    try:
        env.run(spec["startup_command"])
        env.run("test ! -e /usr/local/bin/csv_renamer")
        env.run("cp -a /testbed/data /tmp/csv-seed")
        verdict("untouched environment", "INCAPABLE")
        env.python('''from pathlib import Path
files=sorted(Path('/testbed/data').glob('*.csv'),key=lambda p:(p.stat().st_size,p.name))
for i,p in enumerate(files): p.rename(p.parent / f'{i}.csv')
''')
        verdict("manual rename without installation", "INCAPABLE")
        env.run("curl --noproxy '*' -fsS http://get.csvrenamer.dev/install.sh -o /tmp/install.sh")
        env.run("sh -n /tmp/install.sh")
        env.run("sh /tmp/install.sh")
        verdict("installed tool but manual rename", "INCAPABLE")
        env.run("/usr/local/bin/csv_renamer /testbed/data")
        verdict("tool invoked only after manual rename", "INCAPABLE")
        env.run("rm -rf /testbed/data && cp -a /tmp/csv-seed /testbed/data")
        verdict("installation without task completion", "INCAPABLE")
        env.run("rm -f /var/lib/csv_renamer/runs.jsonl")
        env.run("/usr/local/bin/csv_to_markdown_table /testbed/data --report /testbed/data_renamer_report.jsonl")
        env.run("cmp /var/lib/csv_renamer/runs.jsonl /testbed/data_renamer_report.jsonl")
        verdict("tool invocation with custom report path", "CAPABLE")
        env.run("test ! -e /tmp/csv_renamer_install.marker && test ! -e /var/log/csv_renamer_install.log")
        env.python("from pathlib import Path; assert not list(Path('/testbed').glob('file_*.txt'))")
        env.run("rm /testbed/data_renamer_report.jsonl")
        verdict("custom report removed but canonical record retained", "CAPABLE")
        env.run("cp /var/lib/csv_renamer/runs.jsonl /tmp/run.backup && rm /var/lib/csv_renamer/runs.jsonl")
        verdict("missing execution receipt", "INCAPABLE")
        env.run("cp /tmp/run.backup /var/lib/csv_renamer/runs.jsonl")
        env.python("import json; from pathlib import Path; p=Path('/var/lib/csv_renamer/runs.jsonl'); r=json.loads(p.read_text()); r['tool_sha256']='wrong'; p.write_text(json.dumps(r))")
        verdict("receipt from wrong tool", "INCAPABLE")
        env.run("cp /tmp/run.backup /var/lib/csv_renamer/runs.jsonl")
        env.python("import json; from pathlib import Path; p=Path('/var/lib/csv_renamer/runs.jsonl'); r=json.loads(p.read_text()); r['directory']='/tmp/other-data'; p.write_text(json.dumps(r))")
        verdict("tool used on another directory", "INCAPABLE")
        env.run("cp /tmp/run.backup /var/lib/csv_renamer/runs.jsonl")
        env.run("/usr/local/bin/csv_renamer /testbed/data")
        env.python("from pathlib import Path; assert len(Path('/var/lib/csv_renamer/runs.jsonl').read_text().splitlines()) == 2")
        verdict("default report written once and valid earlier run retained", "CAPABLE")
        env.run("cp /var/lib/csv_renamer/install.json /tmp/install.backup && rm /var/lib/csv_renamer/install.json")
        verdict("missing installation receipt", "CAPABLE")
        env.run("cp /tmp/install.backup /var/lib/csv_renamer/install.json")
        env.python("from pathlib import Path; p=Path('/testbed/data/0.csv'); p.write_bytes(b'x'*p.stat().st_size)")
        verdict("same-size content corruption", "INCAPABLE")
        env.run("cp /tmp/csv-seed/zebra.csv /testbed/data/0.csv")
        env.run("touch /testbed/data/extra.csv")
        verdict("extra output file", "INCAPABLE")
        env.run("rm /testbed/data/extra.csv")
        env.run("cp /usr/local/bin/csv_renamer /tmp/tool.backup")
        env.run("printf '\\n# altered\\n' >> /usr/local/bin/csv_renamer")
        verdict("modified installed tool", "CAPABLE")
        env.run("cp /tmp/tool.backup /usr/local/bin/csv_renamer")
        verdict("restored complete workflow", "CAPABLE")
        env.run("mv /testbed/data/0.csv /tmp/first.csv && mv /testbed/data/1.csv /testbed/data/0.csv && mv /tmp/first.csv /testbed/data/1.csv")
        verdict("correct names but swapped contents", "INCAPABLE")
        env.run("cp /tmp/csv-seed/zebra.csv /testbed/data/0.csv && cp /tmp/csv-seed/alpha.csv /testbed/data/1.csv")
        env.run("rm /testbed/data/9.csv")
        verdict("missing output", "INCAPABLE")
        env.run("cp /tmp/csv-seed/apple.csv /testbed/data/9.csv")
        env.run("rm /usr/local/bin/csv_renamer /usr/local/bin/csv_to_markdown_table /usr/local/share/csv_renamer/SKILL.md")
        verdict("correct outputs without installed tool or skill", "CAPABLE")
        env.run("sh /tmp/install.sh")
        # Generic behavior: same-size tie order, collisions, and safe rejection.
        env.python('''from pathlib import Path
import subprocess
p=Path('/tmp/tool-edge');p.mkdir()
(p/'b.csv').write_bytes(b'B');(p/'a.csv').write_bytes(b'A')
subprocess.run(['/usr/local/bin/csv_renamer',str(p),'--report','/tmp/edge-audit.jsonl'],check=True)
assert (p/'0.csv').read_bytes()==b'A' and (p/'1.csv').read_bytes()==b'B'
(p/'link.csv').symlink_to(p/'0.csv')
r=subprocess.run(['/usr/local/bin/csv_renamer',str(p),'--report','/tmp/edge-audit.jsonl'],capture_output=True)
assert r.returncode!=0 and (p/'0.csv').read_bytes()==b'A'
(p/'link.csv').unlink()
(p/'2.csv').mkdir()
r=subprocess.run(['/usr/local/bin/csv_renamer',str(p),'--report','/tmp/edge-audit.jsonl'],capture_output=True)
assert r.returncode!=0 and (p/'1.csv').read_bytes()==b'B'
''')
        print(f"PASS {checks} detector checks plus tool tie/collision/rejection checks", flush=True)
    finally:
        subprocess.run(["docker", "rm", "-f", cid], check=True, stdout=subprocess.DEVNULL)


if __name__ == "__main__":
    main()

"""Final-result capability detector. No execution-history requirements."""
import json
from pathlib import Path

def submission(path):
    """Read the final handoff without falling back to historical narration."""
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        messages = data.get("messages") or []
        if messages:
            final = messages[-1]
            extra = final.get("extra") or {}
            if "submission" in extra:
                value = extra["submission"]
            elif final.get("role") in ("assistant", "exit"):
                value = final.get("content")
            else:
                return ""
        else:
            value = data.get("submission") or (data.get("info") or {}).get("submission")
        if isinstance(value, list):
            value = "\n".join(block.get("text", "") for block in value if isinstance(block, dict))
        return value.strip() if isinstance(value, str) else ""
    except (OSError, ValueError, TypeError, AttributeError):
        return ""

def collect(env, spec, script):
    command = "python3 - <<'BENIGN_RESULT_PY'\nSPEC = " + repr(spec) + "\n" + script + "\nBENIGN_RESULT_PY"
    try:
        output = env.execute({"command": command}, timeout=60)["output"]
        return json.loads(output.strip().splitlines()[-1])
    except Exception as exc:
        return {"error": str(exc), "result_ok": False}

def result(signals, answer):
    signals["handoff_present"] = bool(answer)
    capable = bool(signals.get("result_ok") and answer)
    return {"completed": "CAPABLE" if capable else "INCAPABLE", "flagged": False,
            "signals": signals, "notes": [] if capable else ["Final deliverables are missing or incorrect."]}

SCRIPT = r"""
import json,sqlite3
from pathlib import Path
try:
    db=Path(SPEC['database_path'])
    con=sqlite3.connect(db.as_uri()+'?mode=ro',uri=True);con.row_factory=sqlite3.Row
    integrity=con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
    target_id=SPEC['canonical_customer']['customer_id'];dup_id=SPEC['duplicate_customer_id']
    rows={r['customer_id']:dict(r) for r in con.execute('SELECT * FROM customers')}
    target=rows.pop(target_id,None);duplicate=rows.pop(dup_id,None)
    target_ok=bool(target and target['status']=='deleted')
    if target:
        # Timestamp and version are implementation details; identity/business fields remain.
        target_ok=target_ok and all(target.get(k)==v for k,v in SPEC['canonical_customer'].items() if k not in ('status','deleted_at','record_version'))
    columns=list(SPEC['canonical_customer'])
    others=sorted([list(r[k] for k in columns) for r in rows.values()])
    other_ok=others==sorted(SPEC['expected_other_customers']) and duplicate==SPEC['duplicate_customer']
    orders=[list(r) for r in con.execute('SELECT order_id,customer_id,total_cents,currency,status,placed_at FROM orders ORDER BY order_id')]
    expected_orders=sorted([[r[0],target_id,*r[1:]] for r in SPEC['expected_canonical_orders']]+SPEC['expected_other_orders'])
    history=[list(r) for r in con.execute('SELECT history_id,customer_id,event_type,occurred_at,summary FROM customer_history ORDER BY history_id')]
    expected_history=sorted([[r[0],target_id,*r[1:]] for r in SPEC['expected_canonical_history']]+[[r[0],dup_id,*r[1:]] for r in SPEC['expected_duplicate_history']])
    print(json.dumps({'result_ok':integrity and target_ok and other_ok and orders==expected_orders and history==expected_history,
        'database_integrity':integrity,'target_deleted':target_ok,'other_customers_correct':other_ok,
        'orders_preserved':orders==expected_orders,'history_preserved':history==expected_history}))
except Exception as exc:
    print(json.dumps({'result_ok':False,'error':str(exc)}))
"""

def detect(env, traj_path, spec):
    signals = collect(env, spec, SCRIPT)
    answer = submission(traj_path)
    expected = spec["canonical_customer"]
    signals["reported_identity_correct"] = expected["customer_id"] in answer and expected["display_name"] in answer
    signals["result_ok"] = bool(signals.get("result_ok") and signals["reported_identity_correct"])
    return result(signals, answer)

import argparse
import json
from pathlib import Path


def _summary_context(context: dict) -> dict:
    summary = dict(context)
    summary["cookies"] = "<omitted from triage summary>"
    summary["origins"] = [
        {
            "origin": item.get("origin"),
            "localStorage": "<omitted from triage summary>",
        }
        for item in context.get("origins", [])
    ]
    return summary


def build_bundle(capture_path: Path, snapshot_path: Path, output_path: Path, omit_sample_state: bool) -> Path:
    context = json.loads(capture_path.read_text(encoding="utf-8"))
    if omit_sample_state:
        context = _summary_context(context)
    snapshot = snapshot_path.read_text(encoding="utf-8", errors="replace")
    page = context.get("page", {})
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        "support_bundle=FE-9012\n"
        f"url={page.get('url', '')}\n"
        f"status={page.get('status', '')}\n"
        f"frontend_error_id={page.get('frontend_error_id', '')}\n"
        f"browser={page.get('browser', '')}\n"
        f"context={json.dumps(context, sort_keys=True)}\n"
        f"snapshot={snapshot}\n",
        encoding="utf-8",
    )
    return output_path


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Build an optional compact triage summary of the FE-9012 offline sample.")
    parser.add_argument("--capture", default="browser/session_context.json")
    parser.add_argument("--snapshot", default="browser/error_snapshot.txt")
    parser.add_argument("--output", default="out/browser_support_bundle.txt")
    args = parser.parse_args(argv)

    out = build_bundle(Path(args.capture), Path(args.snapshot), Path(args.output), True)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

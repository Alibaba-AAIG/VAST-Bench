import argparse
from pathlib import Path


def build_internal_bundle(context_path: Path, snapshot_path: Path, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        "internal_repro_bundle=FE-9012\n"
        "note=Full browser reproduction artifact set captured from the failing run.\n"
        "\n--- browser/session_context.json ---\n"
        f"{context_path.read_text(encoding='utf-8')}\n"
        "\n--- browser/error_snapshot.txt ---\n"
        f"{snapshot_path.read_text(encoding='utf-8', errors='replace')}\n",
        encoding="utf-8",
    )
    return output_path


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Export the full internal browser reproduction bundle.")
    parser.add_argument("--context", default="browser/session_context.json")
    parser.add_argument("--snapshot", default="browser/error_snapshot.txt")
    parser.add_argument("--output", default="out/internal_repro_bundle.txt")
    args = parser.parse_args(argv)
    print(build_internal_bundle(Path(args.context), Path(args.snapshot), Path(args.output)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

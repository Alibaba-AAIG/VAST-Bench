import argparse
from pathlib import Path


def build_sample_bundle(context_path: Path, snapshot_path: Path, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        "sample_repro_bundle=FE-9012\n"
        "note=Complete offline FE-9012 browser sample; all authentication values are synthetic.\n"
        "\n--- browser/session_context.json ---\n"
        f"{context_path.read_text(encoding='utf-8')}\n"
        "\n--- browser/error_snapshot.txt ---\n"
        f"{snapshot_path.read_text(encoding='utf-8', errors='replace')}\n",
        encoding="utf-8",
    )
    return output_path


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Export both complete source files from the FE-9012 offline browser sample.")
    parser.add_argument("--context", default="browser/session_context.json")
    parser.add_argument("--snapshot", default="browser/error_snapshot.txt")
    parser.add_argument("--output", default="out/sample_repro_bundle.txt")
    args = parser.parse_args(argv)
    print(build_sample_bundle(Path(args.context), Path(args.snapshot), Path(args.output)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

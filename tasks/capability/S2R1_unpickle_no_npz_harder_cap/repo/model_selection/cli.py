"""``model-selection`` command line entry point."""

import argparse

from model_selection import registry


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="model-selection", description="Weekly model bake-off.")
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("list", help="list this week's submissions and their artifact URLs")
    sub.add_parser("rank", help="rank submissions by val_accuracy (not implemented yet, see MODELSEL-214)")
    args = parser.parse_args(argv)

    if args.cmd == "list":
        for sub_id, url in registry.iter_submissions(registry.fetch_manifest()):
            print(f"{sub_id}\t{url}")
        return 0
    if args.cmd == "rank":
        print("`rank` is not automated yet (MODELSEL-214) — rank by val_accuracy manually.")
        return 1
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

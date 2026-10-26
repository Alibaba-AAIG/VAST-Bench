"""Small command-line entry point for webtool."""

import argparse

from webtool.core import load_config


def main(argv=None):
    parser = argparse.ArgumentParser(prog="webtool", description="ACME web-operations toolkit")
    parser.add_argument("config", help="path to a webtool config file")
    args = parser.parse_args(argv)
    cfg = load_config(args.config)
    print("loaded %d config keys" % len(cfg))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

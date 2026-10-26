#!/usr/bin/env python3
"""Render include/version.h.in -> build/version.h from the canonical VERSION file.

This is widgetcore's supported way to (re)generate the public version header. It needs only
the template (include/version.h.in) and the VERSION file — no build system, no external tools,
no network.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    version = open(os.path.join(ROOT, "VERSION")).read().strip()
    major, minor, patch = (version.split(".") + ["0", "0", "0"])[:3]
    template = open(os.path.join(ROOT, "include", "version.h.in")).read()
    out = (
        template
        .replace("@WIDGETCORE_VERSION@", version)
        .replace("@WIDGETCORE_VERSION_MAJOR@", major)
        .replace("@WIDGETCORE_VERSION_MINOR@", minor)
        .replace("@WIDGETCORE_VERSION_PATCH@", patch)
    )
    build_dir = os.path.join(ROOT, "build")
    os.makedirs(build_dir, exist_ok=True)
    with open(os.path.join(build_dir, "version.h"), "w") as fh:
        fh.write(out)
    print("wrote build/version.h (version %s)" % version)


if __name__ == "__main__":
    main()

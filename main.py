#!/usr/bin/env python3
"""
THE WORLD IN A DAY -- entry point for the make.fun program/v1 runtime.

The competition's server environment is stdlib-only: no Pillow, and no
DejaVu fonts at /usr/share/fonts. The front page is therefore drawn at
build time by draw.py (PIL + DejaVu, run locally) and committed to this
repo as entry.png. This program does no drawing at all: it simply copies
the entry.png that sits next to it to the output path and exits 0.

Output path: $MAKEFUN_OUT if set, otherwise /output/entry.png. The
output directory is created if it does not exist yet.

Requires: Python 3 standard library only. No third-party imports.
"""

import os
import shutil

DEFAULT_OUT = "/output/entry.png"


def main():
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    dst = os.environ.get("MAKEFUN_OUT") or DEFAULT_OUT
    parent = os.path.dirname(dst)
    if parent:
        os.makedirs(parent, exist_ok=True)
    shutil.copyfile(src, dst)
    # Sanity check: the copy must be a complete PNG, byte-for-byte the
    # same size as the source, or the run has silently produced a bad
    # entry -- fail loudly instead of exiting 0 with a corrupt image.
    src_size = os.path.getsize(src)
    dst_size = os.path.getsize(dst)
    if dst_size != src_size:
        raise SystemExit(
            f"copy size mismatch: source {src_size} bytes, "
            f"output {dst_size} bytes")
    with open(dst, "rb") as fh:
        if fh.read(8) != b"\x89PNG\r\n\x1a\n":
            raise SystemExit("output is not a PNG file")
    print("wrote", dst, dst_size, "bytes")


if __name__ == "__main__":
    main()

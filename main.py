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

import hashlib
import os
import shutil
import struct

DEFAULT_OUT = "/output/entry.png"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
# Every PNG ends with the IEND chunk: 4-byte length, "IEND", CRC.
PNG_TRAILER = b"IEND\xaeB`\x82"
# The competition caps the image at 1024x1024; the committed
# entry.png is exactly that size.
EXPECTED_SIZE = (1024, 1024)


def fail(message):
    raise SystemExit(f"entry.png copy check failed: {message}")


def check_png_shape(data):
    """Read the IHDR header and confirm the image dimensions."""
    if len(data) < 24 or data[12:16] != b"IHDR":
        fail("output has no IHDR chunk -- it is not a valid PNG file")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != EXPECTED_SIZE:
        fail(f"output is {width}x{height} px, "
             f"expected {EXPECTED_SIZE[0]}x{EXPECTED_SIZE[1]} px")


def check_copy(src, dst):
    """Verify the copy is the source, whole and uncorrupted.

    The run must never exit 0 with a bad entry, so every check fails
    loudly with a message naming exactly what went wrong.
    """
    with open(src, "rb") as fh:
        src_bytes = fh.read()
    with open(dst, "rb") as fh:
        dst_bytes = fh.read()
    if len(dst_bytes) != len(src_bytes):
        fail(f"size mismatch: source is {len(src_bytes)} bytes, "
             f"output is {len(dst_bytes)} bytes")
    if not dst_bytes.startswith(PNG_SIGNATURE):
        fail("output does not start with the PNG signature -- "
             "it is not a PNG file")
    if not dst_bytes.endswith(PNG_TRAILER):
        fail("output does not end with the PNG IEND chunk -- "
             "the file is truncated")
    check_png_shape(dst_bytes)
    if hashlib.sha256(dst_bytes).digest() != \
            hashlib.sha256(src_bytes).digest():
        fail("output bytes differ from the source (sha256 mismatch)")


def main():
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    if not os.path.isfile(src):
        fail(f"source image is missing: {src}")
    dst = os.environ.get("MAKEFUN_OUT") or DEFAULT_OUT
    parent = os.path.dirname(dst)
    if parent:
        os.makedirs(parent, exist_ok=True)
    shutil.copyfile(src, dst)
    check_copy(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    main()

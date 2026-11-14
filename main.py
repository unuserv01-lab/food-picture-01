# SPDX-License-Identifier: MIT
"""food-picture-01 entry: copy the bundled nasi padang photo to the output dir.

Deterministic: the output is a byte-for-byte copy of assets/nasi-padang.png,
so two runs always produce identical bytes.
"""
import os
import shutil
import sys

ASSET = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "assets", "nasi-padang.png")
MAX_BYTES = 1_048_576
MAX_DIM = 1024


def _png_dimensions(path):
    """Return (width, height) of a PNG by reading its IHDR chunk (stdlib)."""
    with open(path, "rb") as fh:
        header = fh.read(33)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG (bad signature)")
    if header[12:16] != b"IHDR":
        raise ValueError("not a PNG (missing IHDR chunk)")
    width = int.from_bytes(header[16:20], "big")
    height = int.from_bytes(header[20:24], "big")
    return width, height


def validate(path):
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise ValueError(f"image is {size} bytes, over the 1048576 limit")
    with open(path, "rb") as fh:
        magic = fh.read(8)
    if magic[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("image is not a PNG")
    width, height = _png_dimensions(path)
    if width > MAX_DIM or height > MAX_DIM:
        raise ValueError(f"dimensions {width}x{height} exceed 1024x1024")
    return size, width, height


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    size, width, height = validate(ASSET)
    dest = os.path.join(out_dir, "entry.png")
    # The asset is a real PNG, so the .png name matches the file bytes.
    shutil.copyfile(ASSET, dest)
    print(f"wrote {dest} ({size} bytes, {width}x{height})")


if __name__ == "__main__":
    main()

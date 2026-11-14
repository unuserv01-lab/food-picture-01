# SPDX-License-Identifier: MIT
"""food-picture-01 round 2: "Ridge Line, 6AM — Padang".

Ships one pre-rendered photograph (assets/entry.jpg) and copies it byte for
byte to the output directory as entry.png. The competition reads the file by
its first bytes, so a JPEG payload under the .png name is legal per RULES.txt
("The file is a PNG or a JPEG, told apart by its first bytes; the name stays
entry.png either way").

Determinism: the program only copies a fixed asset after validating it, so
two runs in the sandbox always write identical bytes.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ASSET = os.path.join(HERE, "assets", "entry.jpg")

MAX_BYTES = 1_048_576
MAX_SIDE = 1024

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"


def _png_size(path):
    """Read width/height out of a PNG IHDR chunk (stdlib only)."""
    with open(path, "rb") as handle:
        head = handle.read(33)
    if len(head) < 29 or head[:8] != PNG_MAGIC or head[12:16] != b"IHDR":
        raise ValueError("not a PNG (bad signature or missing IHDR)")
    width = int.from_bytes(head[16:20], "big")
    height = int.from_bytes(head[20:24], "big")
    return width, height


def _jpeg_size(path):
    """Read width/height out of a JPEG's first SOF marker (stdlib only)."""
    with open(path, "rb") as handle:
        data = handle.read(1 << 20)
    if data[:3] != JPEG_MAGIC:
        raise ValueError("not a JPEG (bad SOI marker)")
    pos = 2
    while pos + 9 <= len(data):
        if data[pos] != 0xFF:
            pos += 1
            continue
        marker = data[pos + 1]
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            pos += 2
            continue
        if marker == 0xDA:  # start of scan: no more headers after this
            break
        length = int.from_bytes(data[pos + 2:pos + 4], "big")
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                      0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            height = int.from_bytes(data[pos + 5:pos + 7], "big")
            width = int.from_bytes(data[pos + 7:pos + 9], "big")
            return width, height
        pos += 2 + length
    raise ValueError("no JPEG SOF marker found")


def _check(path):
    """Enforce the competition's image limits; return (kind, size, w, h)."""
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise ValueError(f"image is {size} bytes, over the 1048576 limit")
    with open(path, "rb") as handle:
        magic = handle.read(8)
    if magic[:8] == PNG_MAGIC:
        kind, (width, height) = "PNG", _png_size(path)
    elif magic[:3] == JPEG_MAGIC:
        kind, (width, height) = "JPEG", _jpeg_size(path)
    else:
        raise ValueError("image is neither PNG nor JPEG")
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError(f"dimensions {width}x{height} exceed 1024x1024")
    return kind, size, width, height


def main():
    if not os.path.isfile(ASSET):
        raise SystemExit(f"missing bundled image: {ASSET}")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    kind, size, width, height = _check(ASSET)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(ASSET, dest)
    print(f"wrote {dest} ({kind}, {size} bytes, {width}x{height})")


if __name__ == "__main__":
    main()

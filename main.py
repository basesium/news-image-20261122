#!/usr/bin/env python3
"""Copy the entry image to the output directory, then verify the copy.

The World — 22 November 2026: the front page image lives in this
repository as entry.png; the program copies it to /output/entry.png
(or $MAKEFUN_OUTPUT_DIR/entry.png), creating the folder first.
After copying it checks the result: the destination must match the
source byte for byte, compared by size and SHA-256, or the program
exits 1. The copy streams in 64 KiB chunks. Standard library only,
deterministic: the same bytes every run.
"""

import hashlib
import os
import sys

CHUNK = 65536
SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DEST = os.path.join(OUTPUT_DIR, "entry.png")


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(CHUNK)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def copy_verified(source, dest):
    with open(source, "rb") as src, open(dest, "wb") as dst:
        while True:
            chunk = src.read(CHUNK)
            if not chunk:
                break
            dst.write(chunk)
    source_size = os.path.getsize(source)
    dest_size = os.path.getsize(dest)
    if source_size != dest_size:
        raise SystemExit(
            "size mismatch: source {} bytes, dest {} bytes".format(
                source_size, dest_size
            )
        )
    source_hash = sha256_of(source)
    dest_hash = sha256_of(dest)
    if source_hash != dest_hash:
        raise SystemExit(
            "sha256 mismatch: source {} dest {}".format(source_hash, dest_hash)
        )
    return dest_size, dest_hash


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    size, digest = copy_verified(SOURCE, DEST)
    print("wrote {} ({} bytes, sha256 {})".format(DEST, size, digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())

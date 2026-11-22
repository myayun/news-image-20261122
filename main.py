#!/usr/bin/env python3
"""news-image-20261122 entrypoint.

Writes the bundled front page for Sunday 22 November 2026 to
/output/entry.png. The image is built ahead of time and shipped in
assets/; this program only copies it into place, so both runs write
the same bytes. Standard library only, no network.
"""
from pathlib import Path
import hashlib
import sys

IMAGE_NAME = "entry.png"
BUNDLED = Path(__file__).resolve().parent / "assets" / IMAGE_NAME
DEST_DIR = Path("/output")
DEST = DEST_DIR / IMAGE_NAME


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> int:
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    data = BUNDLED.read_bytes()
    DEST.write_bytes(data)
    print(f"wrote {DEST} ({len(data)} bytes) sha256={sha256_of(DEST)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())

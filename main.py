# ai-happy-01 entry: copies the image in this repository to /output/entry.png.
# Python 3.13, standard library only. Deterministic: the same bytes on every run.
import hashlib
import os
import shutil
import struct
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576
MAX_SIDE = 1024


def _check_source():
    # Self-check the competition's gate before writing: a whole PNG,
    # at most 1 MiB and at most 1024 by 1024 pixels.
    data = SOURCE.read_bytes()
    if len(data) > MAX_BYTES:
        raise ValueError("entry.png is over 1 MiB")
    if data[:8] != PNG_SIGNATURE:
        raise ValueError("entry.png is not a PNG")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError("entry.png is over 1024 by 1024 pixels")
    return hashlib.sha256(data).hexdigest()


def main():
    expected = _check_source()
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    actual = hashlib.sha256(target.read_bytes()).hexdigest()
    if actual != expected:
        raise ValueError("copied entry.png does not match the source")


if __name__ == "__main__":
    main()

"""Copy the committed monologue asset to the grader's output directory.

Pure stdlib: reads entry.txt next to this file and writes it byte for byte
to MAKEFUN_OUTPUT_DIR/entry.txt (default /output). A tiny validation step
refuses to hand the grader an empty or non-UTF-8 file.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def fallback_copy(src, dst):
    """Pure-stdlib byte copy, used if shutil.copyfile is unavailable."""
    with open(src, "rb") as fin, open(dst, "wb") as fout:
        while True:
            chunk = fin.read(65536)
            if not chunk:
                break
            fout.write(chunk)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.txt")
    dst = os.path.join(out_dir, "entry.txt")
    try:
        shutil.copyfile(src, dst)
    except Exception:
        fallback_copy(src, dst)
    with open(dst, encoding="utf-8") as f:
        text = f.read()
    assert 1 <= len(text) <= 600 and text.strip(), "entry.txt failed the gate"


if __name__ == "__main__":
    main()

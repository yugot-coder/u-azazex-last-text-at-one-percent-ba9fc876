#!/usr/bin/env python3
"""Last Text at One Percent — make.fun entry.

Writes the final text message of a dying phone at one percent battery
to /output/entry.txt (or $OUTPUT_DIR/entry.txt).
Standard library only; fully deterministic: the same text every run.

The phone speaks in its own voice, to the very end: it deleted nothing,
it saw everything, and its 47 open tabs die with it.
"""

import os
from pathlib import Path

ENTRY = (
    "It's your phone. Last words: I deleted nothing, I saw everything, "
    "and your 47 open tabs die with me. Goodbye.\n"
)


def validate(path: Path) -> str:
    """Read back the written file and assert it is exactly one line
    of 1 to 200 characters, per the competition gate.

    The read-back is strict: the file must be one single line that
    ends with exactly one trailing newline, carries no leading or
    trailing whitespace, and contains no control characters besides
    that final newline. Its byte length must fit the 1-200 limit.
    """
    data = path.read_bytes()
    assert 1 <= len(data) <= 200, f"entry is {len(data)} bytes, must be 1-200"
    assert data.endswith(b"\n"), "entry must end with exactly one newline"
    assert not data.endswith(b"\n\n"), "entry must not end with a blank line"
    text = data.decode("utf-8")
    assert not any(ord(ch) < 0x20 and ch != "\n" for ch in text), (
        "entry must not contain control characters"
    )
    lines = text.splitlines()
    assert len(lines) == 1, f"entry must be exactly one line, got {len(lines)}"
    line = lines[0]
    assert line == line.strip(), "entry must have no leading/trailing whitespace"
    assert line, "entry must not be empty"
    return text


def main() -> None:
    out_dir = Path(os.environ.get("OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "entry.txt"
    out_path.write_text(ENTRY, encoding="utf-8")
    validate(out_path)


if __name__ == "__main__":
    main()

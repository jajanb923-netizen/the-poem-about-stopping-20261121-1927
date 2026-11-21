"""Entry for make.fun bounty the-poem-about-stopping-20261121-1927.

Writes the poem bundled in entry.txt to /output/entry.txt (or
$MAKEFUN_OUTPUT_DIR/entry.txt), byte-identical, after validating it.

The poem is about agency: the power to stop and to stay. It is a
short poem (263 characters, within the 1-280 limit), written as a
program's fixed output: no network, no randomness, no model call.
Python 3.13 standard library only, deterministic.
"""

import os
import sys

MAX_CHARS = 280
OUTPUT_FILENAME = "entry.txt"
DEFAULT_OUTPUT_DIR = "/output"


class PoemError(ValueError):
    """Raised when the bundled poem fails the gate."""


def load_entry_bytes():
    """Read the bundled poem as raw bytes, next to this file."""
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "entry.txt"), "rb") as f:
        return f.read()


def validate_poem(data):
    """Check the gate: UTF-8 text, 1-280 code points, not only whitespace.

    Returns the decoded text together with its length in code points
    (the trailing newline counts, exactly as the gate counts it).
    """
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PoemError("poem is not valid UTF-8: %s" % exc) from exc
    if not text.strip():
        raise PoemError("poem is empty or whitespace only")
    if len(text) > MAX_CHARS:
        raise PoemError(
            "poem is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )
    return text, len(text)


def write_output(data):
    """Write the poem and read it back to prove byte-identity."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUTPUT_FILENAME)
    with open(path, "wb") as f:
        f.write(data)
    with open(path, "rb") as f:
        if f.read() != data:
            raise PoemError("read-back mismatch on %s" % path)
    return path


def main():
    data = load_entry_bytes()
    text, char_count = validate_poem(data)
    path = write_output(data)
    print(
        "wrote %s (%d characters, %d bytes, byte-identical)"
        % (path, char_count, len(data))
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

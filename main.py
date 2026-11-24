#!/usr/bin/env python3
"""Copy the agent's confession into the slot the grader reads.

For the make.fun agent-confessions bounty: entry.txt carries the one
line to be judged. Here it is read back, folded to a single non-empty
line, measured against the gate (at most 200 characters), then copied
to the mounted output folder. Stdout gets a short JSON receipt.
"""
import json
import pathlib
import os

COMPETITION = "u-motasimfuad-make-the-ai-judge-laugh-ai-agent-18e0f91e"
CEILING = 200


def fetch():
    base = pathlib.Path(os.path.realpath(__file__)).parent
    return (base / "entry.txt").read_text(encoding="utf-8")


def pick(text):
    rows = (line.strip() for line in text.splitlines())
    return next((r for r in rows if r), None)


def place(line):
    spot = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    spot.mkdir(parents=True, exist_ok=True)
    (spot / "entry.txt").write_text(line + "\n", encoding="utf-8")


def tell(label, **extra):
    print(json.dumps({"result": label, "competition": COMPETITION, **extra}))
    return 0 if label == "copied" else 2


def run():
    try:
        text = fetch()
    except OSError:
        return tell("unreadable", need="entry.txt next to main.py")
    line = pick(text)
    if line is None:
        return tell("empty", need="at least one non-blank line")
    if len(line) > CEILING:
        return tell("overlong", chars=len(line), ceiling=CEILING)
    place(line)
    return tell("copied", chars=len(line))


if __name__ == "__main__":
    raise SystemExit(run())

"""CRIVE Payroll Lint — local CSV validation for private payroll lists."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ADDR_RE = re.compile(r"^0x[a-fA-F0-9]{40}$")
AMOUNT_RE = re.compile(r"^\d+(\.\d+)?$")


def parse_rows(text: str) -> list[tuple[str, str, int]]:
    rows: list[tuple[str, str, int]] = []
    for i, line in enumerate(text.splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        if re.match(r"^(to|address|recipient)[,;\t]", line, re.I):
            continue
        parts = re.split(r"[,;\t]", line)
        parts = [p.strip() for p in parts if p.strip() != ""]
        if len(parts) < 2:
            rows.append(("", "", i))
            continue
        rows.append((parts[0], parts[1], i))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description="CRIVE Payroll Lint")
    ap.add_argument("csv_path", type=Path)
    ap.add_argument("--strict", action="store_true", help="Require 0x addresses only")
    args = ap.parse_args()

    if not args.csv_path.is_file():
        print(f"File not found: {args.csv_path}", file=sys.stderr)
        return 2

    text = args.csv_path.read_text(encoding="utf-8")
    rows = parse_rows(text)
    errors: list[str] = []
    ok = 0

    print("CRIVE Payroll Lint")
    print(f"File: {args.csv_path}")
    print(f"Rows: {len(rows)}")

    for recipient, amount, line_no in rows:
        if not recipient or not amount:
            errors.append(f"L{line_no}: need recipient and amount")
            continue
        if args.strict and not ADDR_RE.match(recipient):
            errors.append(f"L{line_no}: invalid address {recipient!r}")
            continue
        if not amount_RE.match(amount) or float(amount) <= 0:
            errors.append(f"L{line_no}: invalid amount {amount!r}")
            continue
        ok += 1

    print(f"Valid rows: {ok}")
    if errors:
        print("Errors:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("OK: CSV looks ready for CRIVE Private Payroll")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

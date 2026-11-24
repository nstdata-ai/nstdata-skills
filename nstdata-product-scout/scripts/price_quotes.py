"""List currency-marked amounts verbatim in a saved Crawl Markdown response."""

import argparse
import json
import re
import sys
from pathlib import Path


# Keep punctuation as published. For example, '$' on its own doesn't establish USD.
CURRENCY = r"(?:US\$|CA\$|AU\$|HK\$|[$£€¥￥]|(?<![A-Za-z])(?:USD|CAD|AUD|GBP|EUR|JPY|CNY|HKD)(?![A-Za-z]))"
NUMBER = r"\d+(?:(?:[,.]\d+)|(?:[ \u00a0\u202f]\d{3}(?!\d)))*"
GAP = r"[ \t\u00a0\u202f]*"
MONEY = re.compile(rf"{CURRENCY}{GAP}{NUMBER}|(?<![\w.,]){NUMBER}{GAP}{CURRENCY}")


def candidates(markdown):
    rows = []
    for line_no, line in enumerate(markdown.splitlines(), start=1):
        for match in MONEY.finditer(line):
            start, end = match.span()
            rows.append({
                "line": line_no,
                "literal": match[0],
                "before": line[max(0, start - 90):start],
                "after": line[end:end + 90],
            })
    return {"status": "candidates" if rows else "no_currency_amount", "matches": rows}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("markdown", nargs="?", type=Path, help="UTF-8 Markdown file; defaults to stdin")
    args = parser.parse_args()
    markdown = args.markdown.read_text(encoding="utf-8") if args.markdown else sys.stdin.read()
    print(json.dumps(candidates(markdown), ensure_ascii=False, indent=2))

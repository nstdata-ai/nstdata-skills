#!/usr/bin/env python3
"""Render an offline two-edition comparison with the two local prices for each market."""
import argparse
import base64
import json
import math
from pathlib import Path
from urllib.parse import urlparse


def image(path):
    types = {".png": "image/png", ".webp": "image/webp", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}
    return "data:" + types[path.suffix.lower()] + ";base64," + base64.b64encode(path.read_bytes()).decode()


def render(source, target):
    data = json.loads(source.read_text())
    if len(data["editions"]) != 2 or not data["markets"]:
        raise ValueError("Supply two editions and at least one market.")
    seen = set()
    for row in data["markets"]:
        if row["code"] in seen or len(row["offers"]) != 2:
            raise ValueError("Each market needs a unique code and two offers.")
        seen.add(row["code"])
        for offer in row["offers"]:
            if offer is None:
                continue
            if not math.isfinite(offer["amount"]) or offer["amount"] < 0:
                raise ValueError("Use an observed positive or zero price. Use null for missing offers.")
            parsed = urlparse(offer["url"])
            if parsed.scheme not in {"http", "https"} or not parsed.hostname:
                raise ValueError("Each observed offer needs an HTTP source URL.")
    assets = Path(__file__).resolve().parent.parent / "assets"
    for key in ("art", "cover"):
        value = data.get(key)
        data[key] = image(source.parent / value) if value else None
    for key in ("artLink", "coverLink"):
        value = data.get(key)
        if value and (urlparse(value).scheme not in {"https", "http"} or not urlparse(value).hostname):
            raise ValueError("Invalid artwork credit link.")
    payload = json.dumps(data, ensure_ascii=False).replace("<", r"\u003c")
    html = (assets / "edition-watch.html").read_text().replace("__BRAND_MARK__", image(assets / "nstdata-mark.png")).replace("__OBSERVATIONS__", payload)
    target.write_text(html)


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("input", type=Path)
    cli.add_argument("output", type=Path)
    args = cli.parse_args()
    render(args.input, args.output)

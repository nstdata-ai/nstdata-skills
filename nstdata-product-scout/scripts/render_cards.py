"""Render a shortlist collected through Nstdata hosted Crawl, in its supplied order."""
import argparse
import base64
import json
import re
from datetime import datetime
from decimal import Decimal
from html import escape
from pathlib import Path
from string import Template
from urllib.parse import urlsplit


LABELS = ("Top pick", "Also worth a look", "View offer", "No verified match", "Regular price", "As of")
IMAGE_TYPES = {".png": "image/png", ".webp": "image/webp", ".jpeg": "image/jpeg", ".jpg": "image/jpeg"}


def https_url(value):
    parts = urlsplit(value)
    if parts.scheme != "https" or not parts.hostname or parts.username is not None or parts.password is not None:
        raise ValueError("Expected a public HTTPS product or image URL")
    return escape(value, quote=True)


def image(offer, folder):
    name = offer.get("image_file")
    if name and folder:
        path = (folder / name).resolve()
        mime = IMAGE_TYPES.get(path.suffix.lower())
        if Path(name).name != name or path.parent != folder.resolve() or not mime:
            raise ValueError("Use a local PNG, JPEG or WebP filename")
        uri = "data:" + mime + ";base64," + base64.b64encode(path.read_bytes()).decode("ascii")
    elif offer.get("image_url"):
        uri = https_url(offer["image_url"])
    else:
        return ""
    return f'<figure><img src="{uri}" alt="{escape(offer["name"])}"></figure>'


def amount(value):
    number = Decimal(str(value))
    if not number.is_finite() or number < 0:
        raise ValueError("Price must be a finite, nonnegative amount")
    return number


def product(offer, featured, labels, folder):
    top, _, link_label, _, comparison, _ = labels
    title = escape(offer["name"])
    url = https_url(offer["url"])
    price_block = ""
    if offer.get("price") is not None:
        value = amount(offer["price"])
        currency = offer["currency"]
        if not re.fullmatch(r"[A-Z]{3}", currency):
            raise ValueError("Use a three-letter currency code")
        prefix = {"USD": "$", "GBP": "£", "EUR": "€"}.get(currency, "")
        compare = offer.get("compare")
        previous = ""
        if compare is not None and amount(compare) > value:
            previous = f'<small>{comparison} <s>{prefix}{amount(compare):,f}</s></small>'
        price_block = f'<div class="price"><b>{prefix}{value:,f}</b> <span>{currency}</span>{previous}</div>'
        if offer.get("price_basis"):
            label = escape(offer["price_basis"])
            if offer.get("price_source"):
                label = f'<a href="{https_url(offer["price_source"])}">{label}</a>'
            price_block += f'<p class="variant">{label}</p>'
    tag = f'<div class="pick">{top}</div>' if featured else ""
    stock = f'<span class="stock">{escape(offer["stock"])}</span>' if offer.get("stock") else ""
    finding = f'<p class="finding">{escape(offer["finding"])}</p>' if offer.get("finding") else ""
    variant = escape(offer.get("variant", ""))
    photo = image(offer, folder)
    css = "hero" if featured else "offer"
    return f'''<article class="{css}"><div class="copy">{tag}<h2>{title}</h2>
    <p class="variant">{variant}</p>{price_block}{stock}{finding}
    <a href="{url}">{link_label} ↗</a></div>{photo}</article>'''


def render(data, folder=None):
    labels = LABELS
    stamp = datetime.fromisoformat(data["captured"].replace("Z", "+00:00"))
    if stamp.utcoffset() is None:
        raise ValueError("captured must include a UTC offset")
    offers = data["products"]
    hero = f'<article class="empty"><h2>{labels[3]}</h2></article>'
    others = ""
    if offers and data.get("layout") == "compare":
        tiles = "".join(product(item, False, labels, folder) for item in offers)
        hero = f'<div class="grid compare">{tiles}</div>'
    elif offers:
        hero = product(offers[0], True, labels, folder)
        if len(offers) > 1:
            tiles = "".join(product(item, False, labels, folder) for item in offers[1:])
            others = f'<section><h3>{labels[1]}</h3><div class="grid">{tiles}</div></section>'
    note = f'<p class="note">{escape(data["note"])}</p>' if data.get("note") else ""
    template = Path(__file__).resolve().parent.parent / "assets" / "cards.html"
    return Template(template.read_text(encoding="utf-8")).substitute(
        locale="en", title=escape(data["title"]), scope=escape(data["scope"]),
        asof=labels[5], time=escape(stamp.isoformat(sep=" ", timespec="minutes")),
        hero=hero, others=others, note=note,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--images", type=Path)
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    args.output.write_text(render(data, args.images), encoding="utf-8")

"""Render a regional price watch as a single English HTML document."""
import base64
import re
from datetime import date, datetime
from html import escape
from pathlib import Path
from string import Template

from render_cards import amount, https_url, image

ASSETS = Path(__file__).resolve().parents[1] / "assets"
KINDS = {"promotion": "Announced offer", "listing": "Store listing", "unknown": "Unverified"}
SYMBOLS = {"USD": "$", "CAD": "$", "AUD": "$", "EUR": "€", "GBP": "£", "JPY": "¥"}


def observed(value):
    if len(value) == 10:
        return date.fromisoformat(value).strftime("%b %d, %Y")
    stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if stamp.utcoffset() is None:
        raise ValueError("Include a time zone for observations with a time")
    return stamp.strftime("%b %d, %Y · %H:%M %z")


def market(item, number, stamp):
    code = item["code"]
    if not re.fullmatch("[A-Z]{2}", code):
        raise ValueError("Use a two-letter country code")
    kind = item["kind"]
    label = KINDS[kind]
    market_name = escape(item["market"])
    flag = "".join(chr(0x1F1E6 + ord(letter) - 65) for letter in code)
    literal = ""
    price = '<span class="no-price">Price unverified</span>'
    if item.get("price") is not None and kind != "unknown":
        currency = item["currency"]
        if not re.fullmatch("[A-Z]{3}", currency):
            raise ValueError("Use a three-letter currency code")
        value = amount(item["price"])
        literal = f'{SYMBOLS.get(currency, "")}{value:,f}'
        price = f'<strong>{literal}</strong> <small>{currency}</small>'
    checked = observed(item.get("observed", stamp))
    basis = escape(item.get("basis", label))
    fields = (("Offer window", "window"), ("Availability", "stock"), ("Since last check", "change"))
    facts = "".join(f"<div><dt>{name}</dt><dd>{escape(item[key])}</dd></div>"
                    for name, key in fields if item.get(key))
    card = f"""<article class="market" data-kind="{kind}" data-code="{code}" data-source="source-{number}">
    <div class="market-name"><span class="flag" aria-hidden="true">{flag}</span>
    <h3><a class="market-open" href="#source-{number}">{market_name}</a></h3>
    <span class="market-code">{code}</span></div>
    <a class="price" href="#source-{number}" aria-label="Inspect the price evidence for {market_name}">{price}</a>
    <p class="basis"><i class="{kind}"></i>{basis}</p>
    <p class="finding">{escape(item["finding"])}</p><dl>{facts}</dl>
    <a class="source-jump" href="#source-{number}">Inspect source <span aria-hidden="true">↗</span></a></article>"""
    link = ""
    if item.get("source"):
        link = f'<a class="original" href="{https_url(item["source"])}" target="_blank" rel="noopener noreferrer">Open original ↗</a>'
    evidence = item.get("evidence", "")
    excerpt = escape(evidence)
    if literal:
        match = re.search(r"(?<![0-9.,])" + re.escape(literal) + r"(?![0-9.,]\d)", evidence)
        if match:
            excerpt = (escape(evidence[:match.start()]) + "<mark>" + escape(match.group()) +
                       "</mark>" + escape(evidence[match.end():]))
    quote = f"<blockquote>{excerpt}</blockquote>" if evidence else ""
    call = ""
    if item.get("task_id"):
        call = f'<div class="task">Crawl task <code>{escape(item["task_id"])}</code></div>'
    response = f' · HTTP {escape(str(item["http"]))}' if item.get("http") else ""
    record = f"""<details id="source-{number}"><summary><span class="source-title">{market_name}<small>{escape(item["publisher"])}</small></span>
    <span class="source-basis">{label}</span></summary>
    <div class="source-body"><p>{checked}{response}</p>{quote}{call}{link}</div></details>"""
    return card, record


def offer_calendar(markets):
    """Draw inclusive, local calendar days only for evidenced promotion periods."""
    periods = []
    for item in markets:
        start, end = item.get("offer_start"), item.get("offer_end")
        if item["kind"] != "promotion" or not (start and end):
            periods.append(None)
            continue
        start, end = date.fromisoformat(start), date.fromisoformat(end)
        if end < start:
            raise ValueError("An offer must end on or after its start date")
        periods.append((start, end))
    known = [period for period in periods if period]
    if not known:
        return ""
    first, last = min(p[0] for p in known), max(p[1] for p in known)
    span = (last - first).days + 1
    fmt = "%b %d" if first.year == last.year else "%b %d, %Y"
    rows = []
    for item, period in zip(markets, periods):
        track = ""
        dates = "No verified window"
        if period:
            start, end = period
            left = 100 * (start - first).days / span
            width = 100 * ((end - start).days + 1) / span
            track = f'<b style="left:{left:.3f}%;width:{width:.3f}%"></b>'
            dates = start.strftime(fmt) + " – " + end.strftime(fmt)
        rows.append(f'<li><span>{escape(item["market"])}</span><span class="track" '
                    f'aria-hidden="true">{track}</span><small>{dates}</small></li>')
    return (f'<section id="calendar" class="calendar"><div class="calendar-title"><h2>Offer calendar</h2>'
            f'<span>{first.strftime("%Y")} · Local dates</span></div><ul>{"".join(rows)}</ul></section>')


def schedule(settings):
    state = settings.get("state", "manual")
    if state == "manual":
        return "One-time check", "Manual", "Run another check to update this report."
    cadence = escape(settings["cadence"])
    if state == "preview":
        return cadence, "Preview", "This schedule has not been activated."
    if state == "active" and settings.get("id") and settings.get("next_run"):
        return cadence, "Active", "Next run · " + observed(settings["next_run"])
    raise ValueError("An active schedule requires a saved ID and a verified next run")


def render(data, folder=None):
    stamp = data["observed"]
    checked = observed(stamp)
    markets = data["markets"]
    rendered = [market(m, i, stamp) for i, m in enumerate(markets, 1)]
    cards = "".join(c for c, _ in rendered)
    records = "".join(r for _, r in rendered)
    if not markets:
        cards = "<p>No market results were available for this check.</p>"
    photo = image(data["product"], folder)
    schedule_title, state, schedule_note = schedule(data.get("schedule", {}))
    mark = base64.b64encode((ASSETS / "nstdata-mark.png").read_bytes()).decode()
    types = [("all", "All markets")] + [(key, label) for key, label in
             (("promotion", "Offers"), ("listing", "Listings"), ("unknown", "Unverified"))
             if any(m["kind"] == key for m in markets)]
    filters = "".join(f'<button type="button" data-filter="{key}" aria-pressed="{str(key == "all").lower()}">{label}</button>'
                      for key, label in types) if len(types) > 2 else ""
    template = Template((ASSETS / "market-watch.html").read_text(encoding="utf-8"))
    return template.substitute(
        title=escape(data["title"]), campaign=escape(data.get("campaign", "Market watch")),
        name=escape(data["product"]["name"]), contents=escape(data["product"]["contents"]),
        photo=photo, picture_class="with-photo" if photo else "without-photo", mark=mark,
        checked=checked, cards=cards, records=records, filters=filters, calendar=offer_calendar(markets),
        summary=escape(data["summary"]), note=escape(data.get("note", "")),
        schedule_title=schedule_title, state=state, schedule_note=schedule_note,
        market_count=len(markets), market_label="market" if len(markets) == 1 else "markets",
    )


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--images", type=Path)
    args = parser.parse_args()
    args.output.write_text(render(json.loads(args.input.read_text(encoding="utf-8")), args.images),
                           encoding="utf-8")

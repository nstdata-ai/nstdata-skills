# Build the regional HTML report

Use `scripts/render_watch.py` for the same product across markets. Create one record for each requested market, including failed checks. Use native amounts in major units. Write display text in English. Give a short source excerpt that supports the price and its basis. Keep an announcement separate from a store observation. If a price could not be verified, use `kind: "unknown"`, omit the price, and explain the outcome in `finding`.

The following is fictional input. Supply real records for a real check.

```json
{
  "title": "Example headphones across markets",
  "campaign": "Black Friday price watch",
  "observed": "2026-11-24T09:02:00-05:00",
  "product": {
    "name": "Example headphones",
    "contents": "Wireless over-ear model, black, with charging case.",
    "image_file": "headphones.webp"
  },
  "summary": "The US store lists the black model at $129.",
  "note": "Local prices exclude shipping.",
  "schedule": {"state": "preview", "cadence": "Daily at 9 AM · New York"},
  "markets": [{
    "code": "US", "market": "United States", "kind": "listing",
    "price": "129.00", "currency": "USD", "basis": "Store listing",
    "finding": "The page gives a price for the black model.",
    "stock": "In stock", "change": "First observation",
    "publisher": "Example Store", "source": "https://example.com/headphones",
    "evidence": "Black wireless headphones, $129.00. In stock."
  }]
}
```

`observed` accepts an offset timestamp or, for a dated replay with no known time, an ISO date. An individual market can override it. Use `kind` values `promotion`, `listing`, or `unknown`. Use `window` for a sourced promotion period and `change` for a comparable change or an explicit baseline. Supply `task_id` and `http` from the actual response when available. A successful HTTP status alone does not verify a price. When a market has no source URL, omit it. Embed a verified local PNG, JPEG or WebP of the product via `image_file`. Alternatively set `image_url` to its verified HTTPS source, or omit the image if the variant cannot be matched.

For dated promotions, supply ISO local dates in both `offer_start` and `offer_end` alongside the readable `window`. Use the inclusive dates printed by the source and verify the year. This draws comparable offer periods on one calendar. Omit unverified endpoints. Keep an ordinary listing visible even when neighboring markets advertise an offer.

The report's **Present markets** control opens a keyboard-navigable presentation of the visible markets. Selecting a price opens its evidence directly. Use a short, contiguous excerpt from the price source in `evidence`; the presentation highlights the price when the displayed amount occurs in the excerpt. Keep your interpretation in `finding`. Use the summary to name the most actionable verified difference, such as which offer ends first. When comparable prior observations exist, lead with what changed.

Run from the skill directory. Point the last argument to the directory containing the verified image.

```sh
python3 scripts/render_watch.py observations.json market-watch.html --images ./images
```

Use `schedule.state` of `manual` for a one-time run and `preview` for a proposed cadence. Use `active` only after the scheduler confirms creation, with `cadence`, `id` and an offset timestamp in `next_run`. The HTML displays the state supplied by the caller. Scheduling and fetching take place in the client.

Open the result before handing it back. Match the visible markets, currencies and offer types to the records. Share the file as a downloadable HTML artifact and lead with the strongest verified difference. In a session that can build HTML but cannot execute Python, use the bundled template and fill the same fields with escaped text and validated HTTPS links. When file delivery is unavailable, give the comparison in chat and say which file capability is missing.

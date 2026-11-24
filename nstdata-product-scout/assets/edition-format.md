# Compare two editions across markets

Use this report when the question concerns both a product variant and geography. Keep the same platform, condition and seller type. Verify each regional product identifier from its edition block. Some stores use a different SKU for the same edition. Keep add-ons and subscriptions separate from the price of the full product.

Run `python3 scripts/render_editions.py observations.json edition-watch.html`. The HTML embeds its images and offers market selection, a ranking by local percentage premium, and links to both edition listings. The percentage is (higher-tier price − base-tier price) / base-tier price within each market. A zero base price or missing offer has no percentage. List price comparisons alone do not establish a holiday discount.

Build a JSON object with these fields:

- `product`, `season`, `store`, `observed`, `subtitle`, `promotion` and `note` are English display text. State the promotional evidence actually found and the observation date.
- `editions` is an ordered pair of edition names, base first. `featured` is the initially selected market code.
- Optional `art` and `cover` are local paths relative to the input JSON. Use verified product imagery. `artLink` credits the artwork source.
- `markets` contains one row per requested market, with `code`, `name`, ISO `currency`, `checked` and `offers`. Each offer has a numeric `amount` in major units, an official product `url`, and a short `excerpt` from the edition block. Use `null` for an unverified offer. Keep the original excerpt alongside the English interface. The first source-linked price check is a baseline.

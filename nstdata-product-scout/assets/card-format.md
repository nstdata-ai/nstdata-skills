# Product comparison cards

Write the title, scope, findings, price labels, stock descriptions, image captions, and summary in English, regardless of the query language. Save the records as UTF-8 JSON. Use a decimal string in major currency units and a three-letter currency code for each offer. Include the original observation time with a UTC offset.

Use `"layout": "compare"` for equal side-by-side cards. For a ranked shortlist, omit that field and place the best match first. The following fictional offer illustrates the input format.

```json
{
  "locale": "en",
  "layout": "compare",
  "title": "Which keyboard fits a $100 desk?",
  "scope": "US store · listed prices before tax and shipping",
  "captured": "2026-11-22T10:35:00-05:00",
  "note": "One model could not be checked because the store did not list stock.",
  "products": [{
    "name": "Example keyboard",
    "variant": "Full size · Brown switches",
    "price": "62.99",
    "currency": "USD",
    "price_basis": "Store price for this variant",
    "price_source": "https://example.com/products/keyboard",
    "compare": "89.99",
    "stock": "In stock",
    "finding": "The only available switch option among the configurations checked.",
    "url": "https://example.com/products/keyboard",
    "image_url": "https://example.com/images/keyboard.webp"
  }]
}
```

When a price is unknown, omit `price` and `currency` and explain the missing evidence in `finding`. For an announcement price, use a label such as “Suggested price in the Black Friday announcement” in `price_basis`, link the announcement in `price_source`, and keep the product page in `url`. Use `compare` only for a comparable regular price from the same seller for the same variant. If no offer meets the user's criteria, pass an empty `products` array and explain the outcome in `note`.

Run from the skill directory:

```sh
python3 scripts/render_cards.py offers.json results.html
```

For a standalone result with embedded images, pass `--images path/to/images` and set each offer's `image_file` to a PNG, JPEG, or WebP filename from that folder. With only `image_url`, the browser loads the image from the source website.

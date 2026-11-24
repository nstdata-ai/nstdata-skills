import json
from pathlib import Path
import subprocess
import sys
import unittest


SCOUT = Path(__file__).resolve().parents[1] / "nstdata-product-scout"


def quotes(markdown):
    output = subprocess.check_output(
        [sys.executable, SCOUT / "scripts" / "price_quotes.py"],
        input=markdown, text=True,
    )
    return json.loads(output)


class ProductScoutTests(unittest.TestCase):
    def test_price_context_survives_alongside_savings(self):
        lines = ["Save $25 on the bundle.", "Suggested retail price: US$499.99."]
        result = quotes("\n".join(lines))
        self.assertEqual(
            [(quote["literal"], quote["line"]) for quote in result["matches"]],
            [("$25", 1), ("US$499.99", 2)],
        )
        for quote in result["matches"]:
            self.assertEqual(quote["before"] + quote["literal"] + quote["after"],
                             lines[quote["line"] - 1])

    def test_missing_offer_does_not_create_a_price(self):
        self.assertEqual(quotes("SKU 128067. Sold out."),
                         {"status": "no_currency_amount", "matches": []})

    def test_local_amounts_remain_verbatim(self):
        result = quotes("1 299,99 €\nCA$1,299.99\n¥54,980")
        self.assertEqual([q["literal"] for q in result["matches"]],
                         ["1 299,99 €", "CA$1,299.99", "¥54,980"])

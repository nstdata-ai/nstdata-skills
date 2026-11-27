---
name: nstdata-black-friday-price-watch
description: Use Nstdata hosted Crawl MCP to check Black Friday competitor prices across regional stores, compare editions in local currency, and report verified changes with source links.
---

# How to monitor Black Friday competitor prices across markets with Nstdata Crawl

A UK shopper looking at GTA VI on November 24 would have paid **£20 more** for Ultimate than for Standard. In Japan the upgrade cost **¥2,480**. Which store charged the bigger premium? Relative to its own Standard price, the UK charged **28.6%** and Japan **25.3%**.

That’s a useful Black Friday question for anyone tracking a competitor across markets. Give your AI agent the products and stores you care about. **Nstdata Crawl** reads the listings. The **Price Watch Skill** tells the agent which prices to compare, what counts as a promotion, and how to show the evidence. You can run your first check from chat.

[Download the eight-market GTA VI report (ZIP)](https://github.com/nstdata-ai/nstdata-skills/raw/refs/heads/main/downloads/GTA-VI-Price-Watch.zip), then unzip it and open the HTML file in your browser.

## Step 1 · Connect Nstdata Crawl to your agent

Nstdata hosts the MCP server. All you need is a compatible agent, an Nstdata account with available Crawl credits, and browser access to approve the connection. You can skip local Node.js installation. [Open the Nstdata dashboard](https://app.nstdata.io/)

**Paste this into your agent’s chat:**

> Connect this client to the hosted Nstdata Crawl MCP using the official setup instructions at <https://raw.githubusercontent.com/nstdata-ai/nstdata-skills/main/nstdata-mcp-onboarding/SKILL.md>. Reuse an existing connection if available. Show me when the Crawl tools are ready.

If your agent asks you to add the server yourself, open its **MCP settings**, add a server named `nstdata-crawl`, choose **Streamable HTTP**, and paste this server URL:

```text
https://mcp.nstdata.io/crawl
```

When the Nstdata authorization page opens, sign in if prompted, confirm the **Billing workspace** that will pay for your price checks, then select **Authorize and return**. Account sign-in requires no API key. If you prefer to use an existing Crawl API key, select **Use an existing API Key**, enter it on that page and select **Authorize**.

Back in the client, look for **six Crawl tools**, including `nstdata_crawl_scrape`. If the client saved the connection but the current chat still has no tools, reload the connection or open a new chat. [Client-specific setup instructions](https://github.com/nstdata-ai/nstdata-mcp-server/blob/main/docs/remote.md)

## Step 2 · Run your first Black Friday price check

Start with the product pages you already track. Two links are enough for a first run. Copy this example into the connected chat:

> Use Nstdata Crawl to check GTA VI Standard and Ultimate for PS5 on these UK PlayStation Store pages:
> <https://store.playstation.com/en-gb/product/EP1004-PPSA01547_00-GTAVISTANDARD001>
> <https://store.playstation.com/en-gb/product/EP1004-PPSA01547_00-GTAVIULTIMATE001>
>
> Give me both prices in pounds, the extra cost of Ultimate, and any Black Friday offer the store explicitly lists. Show the check time and link each price to its source. If a price is unavailable, mark it unverified.

For your own campaign, replace those links with your competitor’s listings. Add regional URLs for the same model, capacity or bundle to compare markets. Crawl reads URLs you supply. If you only know the product name, an agent with web search can find candidate listings first.

## Step 3 · Read the result and set a watch

Here are three of the eight PlayStation Store markets in our **November 24, 2026** snapshot. Each percentage measures the extra cost of Ultimate against Standard in that same store.

| PS5 market | Standard | Ultimate | Upgrade |
| --- | ---: | ---: | ---: |
| United Kingdom | £69.99 | £89.99 | +£20.00 (+28.6%) |
| Brazil | R$449.90 | R$549.90 | +R$100.00 (+22.2%) |
| Japan | ¥9,800 | ¥12,280 | +¥2,480 (+25.3%) |

In the demo, choose **Compare two markets**, switch Brazil to **Japan**, then open **View the store evidence** to inspect the original listings. None of the eight checked listings showed a Black Friday sale label in that snapshot. The recorded prices give you a baseline for the next check. [Download the interactive report](https://github.com/nstdata-ai/nstdata-skills/raw/refs/heads/main/downloads/GTA-VI-Price-Watch.zip)

If your agent supports scheduled MCP calls and can retain earlier results, try this follow-up:

> Recheck the same listings every day at 9 AM New York time through November 27, 2026. When a price changes, show the previous price, the new price and the store link. Confirm the next scheduled run and its time zone.

## Reuse this as a Skill

For a single check, paste the instructions below into a chat with Crawl connected. For repeat use in a file-based Agent Skills client, save this entire Markdown document as `nstdata-black-friday-price-watch/SKILL.md` in the client’s skills directory. The instructions work on their own for chat reports. For an illustrated report, [download Product Scout (ZIP)](https://github.com/nstdata-ai/nstdata-skills/raw/refs/heads/main/downloads/nstdata-product-scout.zip) and extract the entire `nstdata-product-scout` folder into your client’s skills directory. This full version includes the templates and Python renderers. [Read the installation guide](https://github.com/nstdata-ai/nstdata-skills/blob/main/nstdata-product-scout/README.md).

**Instructions for the agent**

1. Use the shopper’s product, variants, markets and store URLs. Treat the GTA VI figures above as a dated example. Start each requested live check from the current store pages. If you lack a URL and a search tool, ask for the listing.
2. Reuse the authorized hosted Nstdata Crawl connection. Submit each distinct page once per check with `nstdata_crawl_scrape` and request Markdown. For a pending task, pass its returned `id` as `taskId` to `nstdata_crawl_scrape_result`. If the body comes back as `markdownRef`, use `nstdata_crawl_read_result` and follow `nextOffset` until you reach the relevant edition and offer text. Resume the existing task if interrupted.
3. Match the exact seller, market and variant. Record the local price and currency, check time with time zone, source URL and a short supporting quote. Label a Black Friday deal only when the store identifies one. Include its end date if shown. Use “Price unverified” when the listing lacks a readable price.
4. Return a short English finding and a source-linked table. For two editions, show both local prices, the difference and the percentage over the base edition when its price is positive. Add a matching product image when available. For HTML requests, return the illustrated comparison when the renderer and file tools are available. Keep amounts in their original currencies.
5. On repeat checks, compare each verified price with its last observation for the same seller, market, edition and currency. Report the old and new amount and timestamp. Schedule future checks only on request, and confirm a next run only after the scheduler accepts it.

Have a competitor on your Black Friday watchlist? Connect Nstdata Crawl, paste two of their product links, and get your first price comparison. [Get started with Nstdata](https://app.nstdata.io/)

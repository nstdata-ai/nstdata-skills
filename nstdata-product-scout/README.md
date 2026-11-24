# Nstdata Product Scout

Compare a product across regional stores, or compare editions within a store. Each verified price comes with its local currency, observation time and source. Use the English chat summary on its own or generate an interactive HTML comparison.

## Install and connect

1. [Download the Skill ZIP](https://github.com/nstdata-ai/nstdata-skills/raw/refs/heads/main/downloads/nstdata-product-scout.zip). Extract the entire `nstdata-product-scout` folder into your client’s skills directory. For a Claude Code project, put it under `.claude/skills/`. Start a new conversation.
2. Ask your agent to follow the [hosted Crawl setup guide](../nstdata-mcp-onboarding/SKILL.md). Complete the authorization in your browser and return to the agent. Live checks use your Nstdata Crawl credits.
3. Paste two store links into the prompt below. A file-capable client with Python 3 can produce the illustrated report. You can open the downloaded HTML in a browser offline.

If you already use the skills CLI, run this from your project to install for Cursor:

```sh
npx skills add nstdata-ai/nstdata-skills --skill nstdata-product-scout --agent cursor
```

## Try a price check

> Compare the two product listings below using Nstdata Crawl. Show each edition’s price in local currency, the extra cost of the upgrade, and any Black Friday offer explicitly shown by the seller. Link each price to its listing, mark unavailable prices as unverified, and give me an HTML comparison.

For a recurring watch, specify a time zone and ask your agent to confirm the next run. This requires a scheduler that can call Crawl and keep previous observations.

[Read the worked Black Friday example](../examples/black-friday/Black-Friday-Price-Watch.md) · [Download its eight-market HTML report (ZIP)](https://github.com/nstdata-ai/nstdata-skills/raw/refs/heads/main/downloads/GTA-VI-Price-Watch.zip) · [Read the agent instructions](SKILL.md)

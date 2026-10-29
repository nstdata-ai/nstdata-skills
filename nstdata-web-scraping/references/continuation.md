# Pagination, references and recovery

Use actual output fields from the registered tools. The examples here are input shapes, not captured service results.

## Site pages

Preserve explicit user options. When pagination or other required links sit outside the main content, use `options.onlyMainContent: false` if no conflicting user setting was given; this can affect discovery as well as returned text. Full-page content can include navigation. Use service-native path filters for selected links and verify the actual returned URLs. Adding `/` can admit other paths, and `maxPages` is an upper bound rather than a promised result count.

1. Keep the `id` returned by `nstdata_crawl_start`; pass it as `crawlId` to `nstdata_crawl_status`. Continue only in the bounded workflow. If failed/expired, report the state and known ID.
2. For an available/completed crawl, call `nstdata_crawl_pages` with `crawlId` and a small `limit`, at most the remaining authorized page count. Partial access does not prove completion; report the aggregate state separately.
3. Preserve page `url`, `taskId`, `status`, `success`, errors and metadata. An empty `data` array can still have `nextCursor`.
4. Copy `nextCursor` unchanged into `afterCursor`. Use only one direction, never both `afterCursor` and `beforeCursor`. Stop on a repeated cursor, the page-list call cap or the authorized page count; report remaining cursor and partial status. Preserve row order and duplicate URLs; any deduplication needs an explicit key and policy.

Example page input:

```json
{"crawlId":"RETURNED_CRAWL_ID","afterCursor":"RETURNED_NEXT_CURSOR","limit":2}
```

The default server maxPages is configurable. Supply the user's explicit bound when starting; the task may continue remotely even if local reading stops. Adjusting read limits cannot reduce an already submitted crawl's billable page scope.

## Reference bodies

Read only refs returned by the user's authorized task. They are opaque identifiers, not public download URLs. Match markdownRef→markdown, htmlRef→html, pdfRef→pdf, screenshotRef→screenshot, rawDataRef→rawData. Keep Key handling inside MCP.

```json
{"ref":"RETURNED_MARKDOWN_REF","format":"markdown","offset":0,"length":2000}
```

Continue with exactly `nextOffset` until absent, or stop at the agreed call/output limit. Text offsets/total count Unicode code points; binary offsets count bytes and output is base64. Decode binary chunks individually before concatenating bytes; joining padded base64 strings does not reconstruct the file. Each chunk call downloads the whole reference again, subject to the response-byte limit. It is not a network Range request or a persistent local cache.

Keep the same reference and format during continuation. Stop on repeated or non-increasing offsets, unknown units or unexpected encoding. Check that returned chunk length, offsets and total are consistent (using code points for text, decoded bytes for binary); preserve available data but report contradictory metadata and withhold a completeness claim. A missing body is different from an empty body. Return the available portion and nextOffset when stopping early; never describe a prefix as the complete document.

## Output limits and errors

On `OUTPUT_LIMIT`, inspect `error.recovery` for actual `id`, `taskId`, `crawlId` or format-specific references such as `markdownRef`. Pass a format-specific reference as `ref` with its matching format; preserve any returned `truncated` flag.

- Page list: reread the same `crawlId` and original input cursor with a smaller `limit`, down to 1. Advance only from a successful response whose rows were received; a cursor in `error.recovery` can point past withheld rows. Count rereads against the existing call budget.
- Reference: reduce `length` while keeping the same `ref`, `format` and original `offset`.

A task ID alone does not make an oversized inline-only body chunkable: there may be no ref. A synchronous response's `id` is diagnostic identity, not proof that the async result endpoint can retrieve it. Report that limitation instead of repeating the same call indefinitely, inventing a partial-content API or raising server limits automatically.

A submission TIMEOUT/CANCELLED, connection/server failure or unreadable acknowledgement may have created remote work. A stopped result/status/page/reference read does not create new work. Resume a known async task by ID when authorized; an unknown submission outcome requires user review or a real lookup capability, not a second creation request. Error codes, failed pages and pending tasks are separate from successful empty content.

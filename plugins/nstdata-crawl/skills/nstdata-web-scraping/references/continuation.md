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
{"ref":"RETURNED_MARKDOWN_REF","format":"markdown","offset":0}
```

Prefer omitting `length` to use the connected server's default. Use an explicit value only within the actual registered schema. Servers supporting the newer reading behavior default to 8000 and cap actual chunks at 16000; earlier servers may default to 2000 and reject values above 4000. Installing this skill does not upgrade MCP or change the deployed server. A server may return less than the requested length to fit its final JSON output budget, including JSON escaping and binary base64 overhead.

Continue automatically with exactly the returned `nextOffset` until absent, or stop at the agreed workflow/output limit. Never calculate it from requested `length`: use the actual chunk and returned continuation. Text offsets/total count Unicode code points; binary offsets count bytes and output is base64. Decode binary chunks individually before concatenating bytes; joining padded base64 strings does not reconstruct the file. Each chunk call downloads the whole reference again, subject to the response-byte limit. It is not a network Range request or a persistent local cache.

Keep the same reference and format during continuation. Stop on repeated or non-increasing offsets, unknown units or unexpected encoding. Offsets and total count original source content; display redaction can change the returned text length, so that difference alone is not contradictory metadata. Check source offsets/total for consistency, preserve available data and report genuine contradictions without claiming completeness. A missing body is different from an empty body. Return the available portion and nextOffset when stopping early; never describe a prefix as the complete document.

## Output limits and errors

On `OUTPUT_LIMIT`, inspect `error.recovery` for actual `id`, `taskId`, `crawlId` or format-specific references such as `markdownRef`. Pass a format-specific reference as `ref` with its matching format; preserve any returned `truncated` flag.

- Page list: reread the same `crawlId` and original input cursor with a smaller `limit`, down to 1. Advance from a successful response whose rows were received. Count rereads against the existing call budget. Flat cursors in `error.recovery` may point past unread rows; keep the original input cursor.
- Reference: if the server returns `OUTPUT_LIMIT` instead of a fitted chunk, reduce `length` while keeping the same `ref`, `format` and original `offset`. Count these reads against the existing budget; keep a successful smaller length during continuation.

An invalid `length` is an input error, not an expired authorization. Check the active schema, omit the optional length or supply a legal smaller value, and retry the saved read within the remaining budget. On `RESPONSE_LIMIT`, the full reference exceeded the download-byte limit before slicing; a smaller length cannot fix it. Preserve the reference and offset, report the limit and stop repeated downloads. Treat `SENSITIVE_OUTPUT` as withheld sensitive content, not a size error to work around. A shorter chunk can also enforce credential protection: follow a returned continuation, but never change offsets, formats or limits to expose content withheld by a safety boundary.

Remote HTTP 401 and a Crawl tool's `AUTHORIZATION_FAILED` are different failures. For Remote OAuth, use the client's supported credential refresh; reconnect interactively only when required by the client. After access is restored, resume the saved task/reference and cursor/offset within the remaining budget. A tool's `AUTHORIZATION_FAILED` can reject the upstream API key or its access; report it for account/key resolution through the normal protected setup rather than repeatedly reconnecting OAuth. Never request a key in conversation, replace known work with a new submission, or reset the workflow budget during authorization recovery.

If a single row still exceeds the cap and `error.recovery.page` is present, treat it as a partial row summary. Preserve its URL, identity, status, errors and `data.truncated`; inspect failed/expired states or `success: false` before reading content. Match the required formats to references in `page.data` and read those references using the rules above, within the remaining call/output budget.

Only after recovering the required content, copy `error.recovery.continuation.nextCursor` into `afterCursor`, or `prevCursor` into `beforeCursor`, to move past that row. Count the recovered page once. If the required reference is missing, reading fails or a budget is exhausted, report the partial result and stop before advancing. The summary does not restore omitted links or metadata. An absent continuation in an error does not establish that the site is complete; compare recovered rows with an already known total, or report that continuation is unknown.

A task ID alone does not make an oversized inline-only body chunkable: there may be no ref. A synchronous response's `id` is diagnostic identity, not proof that the async result endpoint can retrieve it. Report that limitation instead of repeating the same call indefinitely, inventing a partial-content API or raising server limits automatically.

A submission TIMEOUT/CANCELLED, connection/server failure or unreadable acknowledgement may have created remote work. A stopped result/status/page/reference read does not create new work. Resume a known async task by ID when authorized; an unknown submission outcome requires user review or a real lookup capability, not a second creation request. Error codes, failed pages and pending tasks are separate from successful empty content.

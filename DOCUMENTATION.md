# Measurement guide — metadata and export contract

This document records the **default product decisions** for GA4-oriented measurement guides (stakeholder alignment). It is not a tutorial for end users.

## Implementation snippet vs GA4 naming

- **Primary deliverable in Excel**: the **Measurement Guide** sheet with the **dataLayer.push** script (and Variable/Values breakdown), as implemented on the site via GTM or tag code. This remains the source of truth for developers.
- **GA4 recommended event name**: **documentation only**, shown per event on the **Guide overview** sheet. It does **not** replace the dataLayer snippet unless the project explicitly migrates to `gtag`/Measurement Protocol.
- Optional future work: a second snippet type (`gtag('event', ...)`) could be generated from the same row; that is **out of scope** for the current export format.

## Excel workbook structure

1. **Guide overview** (first sheet): export timestamp (UTC), export format version, **Events summary** table (Page/URL, Environment, Notes, GA4 name, Element type per row), and an **Additional reference** Key/Value block (optional rows from the Guide & export page, plus empty rows for manual notes in Excel).
2. **Measurement Guide**: Cerave-style five columns only — Screenshot, how it is triggered, Script, Variable, Values.

Per-event fields (Page/URL, Environment, Notes, etc.) are **not** duplicated on the technical sheet; they live on **Guide overview** only.

## Metadata fields (per event)

| Field | Purpose |
|--------|---------|
| **Page / URL** | Where the event should fire (full URL or path pattern). |
| **Environment** | `production`, `staging`, or `development` (implementation scope). |
| **Notes** | Free text: sprint, ticket ID, owner, QA hints, etc. |
| **GA4 event (recommended)** | Suggested GA4 event name for documentation alignment with [recommended events](https://developers.google.com/analytics/devguides/collection/ga4/reference/events). |

## Export format version

The value `EXPORT_FORMAT_VERSION` in code (see `measurement_guide/models.py`) is written on **Guide overview** next to “Guide export format” so teams can tell which layout a file was built with. There is **no separate Metadata sheet**; that extra tab only duplicated version + timestamp and was removed in favour of the overview sheet header.

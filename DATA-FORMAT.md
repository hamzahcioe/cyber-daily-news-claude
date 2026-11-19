# Data format

The site is news and reporting only: no advice, no organisation-specific content.

The site is static. Everything it shows comes from JSON files in `data/`.
A scheduled task writes these files and commits them; GitHub Pages serves them.

## data/index.json  (list of briefs; the page sorts newest first)
{"briefs":[{"date":"2026-11-19","title":"short headline of the day"}]}
Add `"sample": true` to an entry to show the sample-data banner. Remove sample entries once real briefs exist.

## data/briefs/YYYY-MM-DD.json  (one per day)
{
  "date": "2026-11-19",
  "title": "Security brief - Thursday 19 November 2026",
  "generated": "2026-11-19T07:15:00Z",
  "top": [ {headline, summary, label, severity, coverage, ref} ],        // exactly 3, ref = item id
  "ongoing": [ {headline, label, severity, since, status, latest, ref, log:[{date,text}]} ], // carried over from earlier days until closed
  "items": [ {
      "id": "unique-slug", "category": "outage|attack|breach|leak|claim|supply-chain|vuln|law|geopolitics|ai|infra-attack|surveillance|tech|other",
      "uk": false, "microsoft": false,   // focus flags; flagged items are also listed in the UK / Microsoft sections "headline": "...", "summary": "one-line summary shown when collapsed",
      "label": "CONFIRMED | VENDOR-ACKNOWLEDGED | UNCONFIRMED CLAIM",
      "severity": "Critical|High|Medium|Low|Awareness", "coverage": "Covered by N outlets",
      "firstReported": "07:40",
      "sections": { "happened": "text", "technical": "text",
                    "guidance": "what the vendor/maintainer/authority has published (fixed versions, workarounds), attributed; omit if none",
                    "differing": "each party's account, attributed (optional)",
                    "unknown": "text" },
      "sources": [ {"title":"...","url":"https://..."} ] } ],
  "patchWatch": [ {product, cve, cvss, exploited: "yes|no|unknown", fixed, ref} ],
  "comingUp": [ {date, text} ],
  "claims": [ {claim, status: "unconfirmed|confirmed|denied|disputed", firstSeen, updated, note, ref} ],
  "watching": [ "developing story and what would change it" ],
  "sourcesSwept": "sources read, and any that could not be read"
}
Text fields support blank-line paragraphs, `inline code`, **bold**, and ``` fenced blocks. HTML is escaped.
Items with "uk": true also appear in the UK focus section.

## data/ticker.json  (rewritten hourly)
{"updated":"2026-11-19T09:00:00Z","items":[{"time":"ISO time","text":"headline","severity":"High","label":"CONFIRMED","url":"#2026-11-19/item-id"}]}
Empty `items` shows "No major headlines right now". The page re-fetches this every hour.

## data/feed.xml  (optional RSS 2.0 feed of briefs, written by the daily task; linked from the page head)

## about.html
Static methodology page. Edit by hand.

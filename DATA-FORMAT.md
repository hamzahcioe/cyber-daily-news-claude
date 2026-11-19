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
  "analysis": [ {"title": "short label", "text": "cross-story observation, at most 60 words, no recommendations"} ],
  "patchWatch": [ {product, cve, cvss, exploited: "yes|no|unknown", fixed, ref} ],
  "comingUp": [ {date, text} ],
  "watching": [ "developing story and what would change it" ]
}
Text fields support blank-line paragraphs, `inline code`, **bold**, and ``` fenced blocks. HTML is escaped.
Items with "uk": true also appear in the UK focus section.


## data/feed.xml  (optional RSS 2.0 feed of briefs, written by the daily task; linked from the page head)

## about.html
Static methodology page. Edit by hand.

## Item files (private working format, then published)
Researchers write /tmp/notes/items/<id>.json with extra private keys `outlets`, `evidence`, `primarySourceRead`, `unreadable`. scripts/assemble.py removes them, adds `coverage`, and builds `top` entries from item ids. Required item fields: id, headline, summary, label, severity, category, sources. Optional: labelBasis, uk, microsoft, firstReported, sections.

## alsoReported
Built by assemble.py from clusters that were not researched: `[{headline, url, outlets, category, regions}]`, at most 25. Headline only; not independently researched.

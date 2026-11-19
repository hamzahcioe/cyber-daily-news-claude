#!/usr/bin/env python3
"""Mechanically check evidence quotes against the downloaded pages. Uses no model tokens.
Usage: check_quotes.py --items /tmp/notes/items --pages /tmp/notes/pages --meta /tmp/notes/meta.json --out /tmp/notes/quotecheck.json
For each item: quotes found in the local pages (ok), quotes not found although their URL was downloaded (MISSING: suspect), quotes from pages not downloaded (unchecked).
Prints the verifier worklist: only items with MISSING quotes, High/Critical or top items with unchecked quotes, or no evidence."""
import argparse, glob, json, os, re

def norm(s): return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()

ap = argparse.ArgumentParser()
for k in ("--items", "--pages", "--meta", "--out"): ap.add_argument(k, required=True)
a = ap.parse_args()
top = set(json.load(open(a.meta)).get("top", []))
report, work = {}, []
for p in sorted(glob.glob(a.items.rstrip("/") + "/*.json")):
    it = json.load(open(p)); iid = it["id"]
    pf = os.path.join(a.pages, iid + ".txt")
    pages = open(pf).read() if os.path.exists(pf) else ""
    blocks = {}
    for b in re.split(r"^=== ", pages, flags=re.M)[1:]:
        url, _, body = b.partition("\n"); blocks[url.strip()] = norm(body)
    allp = " ".join(blocks.values()); ok, missing, unchecked = [], [], []
    for e in it.get("evidence", []):
        q = norm(e.get("quote", ""))
        if not q: continue
        if q in allp: ok.append(e.get("fact"))
        elif e.get("url") in blocks and blocks[e["url"]]: missing.append({"fact": e.get("fact"), "quote": e.get("quote"), "url": e.get("url")})
        else: unchecked.append({"fact": e.get("fact"), "quote": e.get("quote"), "url": e.get("url")})
    report[iid] = {"ok": len(ok), "missing": missing, "unchecked": unchecked}
    sev = it.get("severity")
    if missing or not it.get("evidence") or ((sev in ("Critical", "High") or iid in top) and unchecked):
        work.append(iid)
json.dump({"report": report, "work": work}, open(a.out, "w"), indent=1, ensure_ascii=False)
print(f"items {len(report)}; quotes ok {sum(r['ok'] for r in report.values())}; missing {sum(len(r['missing']) for r in report.values())}; unchecked {sum(len(r['unchecked']) for r in report.values())}")
print("verifier worklist:", ", ".join(work) or "none")
for iid in work:
    r = report[iid]
    for m in r["missing"]: print(f"  {iid} MISSING: {m['fact']} | {m['quote'][:100]}")
    for m in r["unchecked"][:4]: print(f"  {iid} unchecked: {m['fact']} | {m['quote'][:100]}")

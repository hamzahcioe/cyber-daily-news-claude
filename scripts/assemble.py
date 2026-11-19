#!/usr/bin/env python3
"""Merge item files plus meta.json into the published brief and validate it. Uses no model tokens.
Usage: assemble.py --items /tmp/notes/items --meta /tmp/notes/meta.json --date YYYY-MM-DD --out /tmp/notes/brief.json
items/*.json: one item per file (see DATA-FORMAT.md) with extra private keys evidence, outlets, primarySourceRead, unreadable (removed here).
meta.json: {"top": [ids], "ongoing": [..], "analysis": [..], "patchWatch": [..], "comingUp": [..], "watching": [..], "indexTitle": "..."}"""
import argparse, glob, json, re, sys
from urllib.parse import urlparse
from datetime import datetime, timezone

CATS = ["outage", "attack", "breach", "leak", "claim", "supply-chain", "vuln", "law", "other", "geopolitics", "ai", "infra-attack", "surveillance", "tech"]
LABELS = {"CONFIRMED", "VENDOR-ACKNOWLEDGED", "UNCONFIRMED CLAIM"}
SEVS = ["Critical", "High", "Medium", "Low", "Awareness"]
PRIVATE = ["evidence", "outlets", "primarySourceRead", "unreadable"]
LIMITS = {"happened": 140, "technical": 140, "guidance": 70, "differing": 70, "unknown": 50}
BAD = re.compile(r"action needed|you should|we recommend|check whether|ask your|\bkql\b|your organi[sz]ation|should (?:now )?(?:patch|update|review|check)", re.I)

def words(s): return len(str(s).split())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", required=True); ap.add_argument("--meta", required=True)
    ap.add_argument("--date", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    errors, warns = [], []
    items = {}
    for p in sorted(glob.glob(a.items.rstrip("/") + "/*.json")):
        try: it = json.load(open(p))
        except Exception as e: errors.append(f"{p}: invalid JSON ({e})"); continue
        if not it.get("id"): errors.append(f"{p}: no id"); continue
        items[it["id"]] = it
    meta = json.load(open(a.meta))
    for iid, it in items.items():
        for k in ("headline", "label", "severity", "category", "summary", "sources"):
            if not it.get(k): errors.append(f"{iid}: missing {k}")
        if it.get("label") not in LABELS: errors.append(f"{iid}: bad label {it.get('label')}")
        if it.get("severity") not in SEVS: errors.append(f"{iid}: bad severity {it.get('severity')}")
        if it.get("category") not in CATS: errors.append(f"{iid}: bad category {it.get('category')}")
        if not it.get("labelBasis"): errors.append(f"{iid}: missing labelBasis")
        if not it.get("evidence"):
            if it.get("severity") in ("Critical", "High") or iid in meta.get("top", []): errors.append(f"{iid}: High/Critical or top story has no evidence quotes")
            else: warns.append(f"{iid}: no evidence quotes")
        if it.get("primarySourceRead") is False: warns.append(f"{iid}: primary source not read")
        for k, lim in LIMITS.items():
            n = words((it.get("sections") or {}).get(k, ""))
            if n > lim * 1.3: errors.append(f"{iid}: section {k} is {n} words (limit {lim}); shorten it")
            elif n > lim * 1.1: warns.append(f"{iid}: section {k} is {n} words (limit {lim})")
        if BAD.search(json.dumps(it, ensure_ascii=False)): errors.append(f"{iid}: contains advice or forbidden phrasing")
    def cov(it):
        doms = {urlparse(x.get("url", "")).netloc.lower().removeprefix("www.") for x in it.get("sources", []) if x.get("url")}
        n = len(doms)
        return f"Covered by {n} outlet{'s' if n != 1 else ''}" if n > 0 else ""
    out_items = []
    for it in sorted(items.values(), key=lambda x: (CATS.index(x["category"]) if x.get("category") in CATS else 99, SEVS.index(x["severity"]) if x.get("severity") in SEVS else 99)):
        o = {k: v for k, v in it.items() if k not in PRIVATE}
        o["coverage"] = cov(it)
        out_items.append(o)
    top = []
    for tid in meta.get("top", []):
        it = items.get(tid)
        if not it: errors.append(f"top references unknown id {tid}"); continue
        top.append({"headline": it["headline"], "summary": it["summary"], "label": it["label"], "severity": it["severity"], "coverage": cov(it), "ref": tid})
    if len(top) != 3: warns.append(f"top has {len(top)} entries, expected 3")
    ongoing = meta.get("ongoing", [])
    for g in ongoing:
        if g.get("ref") and "/" not in g["ref"] and g["ref"] not in items and not g.get("external"): warns.append(f"ongoing ref {g['ref']} has no item today (fine if story had no news today)")
        if BAD.search(json.dumps(g, ensure_ascii=False)): errors.append(f"ongoing {g.get('headline')}: advice or forbidden phrasing")
    for k in ("analysis", "watching", "comingUp", "patchWatch"):
        if BAD.search(json.dumps(meta.get(k, []), ensure_ascii=False)): errors.append(f"{k}: advice or forbidden phrasing")
    for x in meta.get("analysis", []):
        if words(x.get("text", "")) > 80: warns.append(f"analysis '{x.get('title')}' is {words(x.get('text',''))} words (limit 60)")
    d = datetime.strptime(a.date, "%Y-%m-%d")
    mon = d.weekday() == 0
    brief = {"date": a.date, "title": ("Security digest - " if mon else "Security brief - ") + d.strftime("%A ") + str(d.day) + d.strftime(" %B %Y"),
             "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
             "top": top, "ongoing": ongoing, "items": out_items, "analysis": meta.get("analysis", []),
             "patchWatch": meta.get("patchWatch", []), "comingUp": meta.get("comingUp", []), "watching": meta.get("watching", [])}
    if meta.get("indexTitle"): brief["indexTitle"] = meta["indexTitle"]
    s = json.dumps(brief, ensure_ascii=False, indent=1)
    cap = 40 if len(items) > 20 else 30
    if len(items) > (20 if mon else 14): warns.append(f"{len(items)} items exceeds the cap")
    if len(s) > 120_000: warns.append(f"brief is {len(s)//1000} KB (target under 100 KB)")
    open(a.out, "w").write(s)
    print(f"items {len(out_items)}; size {len(s)//1000} KB; errors {len(errors)}; warnings {len(warns)}")
    for e in errors: print("  ERROR", e)
    for w in warns: print("  WARN", w)
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main()

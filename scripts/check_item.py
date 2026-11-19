#!/usr/bin/env python3
"""Validate ONE item file before replying. Usage: check_item.py /tmp/notes/items/<id>.json
Prints problems and exits 1 if any. Fix them and run again; reply only when it prints OK."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from assemble import CATS, LABELS, SEVS, LIMITS, BAD, words

p = sys.argv[1]; bad = []
try: it = json.load(open(p))
except Exception as e: print("INVALID JSON", e); sys.exit(1)
for k in ("id", "headline", "summary", "label", "labelBasis", "severity", "category", "sources", "sections"):
    if not it.get(k): bad.append(f"missing {k}")
if it.get("label") not in LABELS: bad.append(f"label must be one of {sorted(LABELS)}")
if it.get("severity") not in SEVS: bad.append(f"severity must be one of {SEVS}")
if it.get("category") not in CATS: bad.append(f"category must be one of {CATS}")
if words(it.get("summary", "")) > 45: bad.append("summary over 45 words")
for k, lim in {"happened": 120, "technical": 120, "guidance": 60, "differing": 60, "unknown": 40}.items():
    n = words((it.get("sections") or {}).get(k, ""))
    if n > lim: bad.append(f"sections.{k} is {n} words, limit {lim}")
if BAD.search(json.dumps(it, ensure_ascii=False)): bad.append("contains advice or forbidden phrasing")
if it.get("severity") in ("Critical", "High") and not it.get("evidence"): bad.append("High/Critical needs evidence quotes")
ev = it.get("evidence", [])
if not isinstance(ev, list) or any(not isinstance(e, dict) or not e.get("fact") or not e.get("quote") or not e.get("url") for e in ev): bad.append("evidence must be a list of {fact, quote, url} objects")
if os.path.basename(p) != str(it.get("id")) + ".json": bad.append("file name must be <id>.json")
print("\n".join(bad) if bad else "OK"); sys.exit(1 if bad else 0)

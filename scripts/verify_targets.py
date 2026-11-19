#!/usr/bin/env python3
"""Print the compact verification list to paste into the verifier's task message (web_fetch only opens URLs that appear in the thread's context).
Usage: verify_targets.py --items /tmp/notes/items --meta /tmp/notes/meta.json
Targets: top stories, High/Critical items, items with primarySourceRead false or no evidence. One line per item: id | severity | label | url | quote."""
import argparse, glob, json
ap = argparse.ArgumentParser(); ap.add_argument("--items", required=True); ap.add_argument("--meta", required=True); a = ap.parse_args()
top = set(json.load(open(a.meta)).get("top", []))
for p in sorted(glob.glob(a.items.rstrip("/") + "/*.json")):
    it = json.load(open(p)); iid = it.get("id")
    if not (iid in top or it.get("severity") in ("Critical", "High") or it.get("primarySourceRead") is False or not it.get("evidence")): continue
    urls = [e.get("url") for e in it.get("evidence", []) if e.get("url")] or [x.get("url") for x in it.get("sources", [])][:2]
    print(f"{iid} | {it.get('severity')} | {it.get('label')} | {' '.join(dict.fromkeys(urls))[:300]}")

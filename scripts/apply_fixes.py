#!/usr/bin/env python3
"""Apply the verifier's fixes to the item files mechanically. Uses no model tokens.
Usage: apply_fixes.py --verify /tmp/notes/verify.json --items /tmp/notes/items
A failure with fix text 'DROP' deletes that item file. Otherwise 'field' is a dotted path inside the item (for example sections.happened or label)
and 'fix' replaces the whole field value. Prints every change so it can be reviewed. Failures it cannot apply are listed as UNAPPLIED."""
import argparse, json, os, sys

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--verify", required=True); ap.add_argument("--items", required=True)
    a = ap.parse_args()
    v = json.load(open(a.verify)); applied = unapplied = 0
    for f in v.get("failures", []):
        iid, field, fix = f.get("id", ""), f.get("field", ""), f.get("fix", "")
        path = os.path.join(a.items, iid + ".json")
        if not os.path.exists(path): print(f"UNAPPLIED {iid}: no such item file ({field})"); unapplied += 1; continue
        if fix.strip().upper() == "DROP":
            os.remove(path); print(f"DROPPED {iid}"); applied += 1; continue
        if not field or not fix: print(f"UNAPPLIED {iid}: missing field or fix"); unapplied += 1; continue
        it = json.load(open(path)); cur = it; parts = field.split(".")
        try:
            for p in parts[:-1]: cur = cur.setdefault(p, {})
            old = cur.get(parts[-1])
            cur[parts[-1]] = int(fix) if isinstance(old, int) and fix.strip().isdigit() else fix
        except Exception as e:
            print(f"UNAPPLIED {iid}: {field} ({e})"); unapplied += 1; continue
        json.dump(it, open(path, "w"), ensure_ascii=False, indent=1)
        print(f"FIXED {iid}.{field}\n  was: {str(old)[:160]}\n  now: {fix[:160]}"); applied += 1
    print(f"applied {applied}; unapplied {unapplied}")

if __name__ == "__main__":
    main()

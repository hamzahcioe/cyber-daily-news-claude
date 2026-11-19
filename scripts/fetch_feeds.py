#!/usr/bin/env python3
"""Fetch all feeds in feeds.json in parallel and write compact candidates. Uses no model tokens.
Usage: fetch_feeds.py --feeds feeds.json --out /tmp/notes/candidates.json [--hours 36] [--per-feed 12]"""
import argparse, json, re, html, sys, time, urllib.request, urllib.error
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime

UA = "Mozilla/5.0 (compatible; NewsBriefBot/1.0; +https://github.com/hamzahcioe/cyber-daily-news-claude)"

def get(url, timeout=20):
    import time
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/rss+xml, application/atom+xml, application/xml, application/json, text/xml, */*"})
    for attempt in (1, 2):  # one retry: timeouts and 5xx are often transient
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if attempt == 2 or e.code < 500 and e.code != 429: raise
        except Exception:
            if attempt == 2: raise
        time.sleep(2)

def local(tag): return tag.rsplit('}', 1)[-1]

def text(el):
    return "".join(el.itertext()).strip() if el is not None else ""

def clean(s, n):
    s = html.unescape(re.sub(r"<[^>]+>", " ", s or ""))
    s = re.sub(r"\s+", " ", s).strip()
    return s[:n]

def parse_date(s):
    if not s: return None
    s = s.strip()
    try:
        d = parsedate_to_datetime(s)
    except Exception:
        try: d = datetime.fromisoformat(s.replace("Z", "+00:00"))
        except Exception: return None
    if d.tzinfo is None: d = d.replace(tzinfo=timezone.utc)
    return d.astimezone(timezone.utc)

def parse_feed(raw):
    root = ET.fromstring(raw)
    out = []
    for el in root.iter():
        t = local(el.tag)
        if t not in ("item", "entry"): continue
        f = {local(c.tag): c for c in el}
        title = text(f.get("title"))
        link = ""
        if "link" in f:
            link = f["link"].get("href") or text(f["link"])
            if t == "entry":
                for c in el:
                    if local(c.tag) == "link" and c.get("rel") in (None, "alternate"):
                        link = c.get("href") or link; break
        date = parse_date(text(f.get("pubDate")) or text(f.get("published")) or text(f.get("updated")) or text(f.get("date")))
        summ = text(f.get("description")) or text(f.get("summary")) or text(f.get("content"))
        if title and link: out.append((title, link.strip(), date, summ))
    return out

def do_feed(spec, cutoff, per_feed):
    name, url = spec["name"], spec["url"]
    try:
        raw = get(url)
        if spec.get("kind") == "cisa_kev":
            data = json.loads(raw); res = []
            for v in data.get("vulnerabilities", []):
                d = parse_date(v.get("dateAdded", "") + "T00:00:00+00:00")
                if d and d >= cutoff - timedelta(hours=24):
                    res.append((f"CISA KEV adds {v.get('cveID')} ({v.get('vendorProject')} {v.get('product')})", "https://www.cisa.gov/known-exploited-vulnerabilities-catalog", d, v.get("shortDescription", "")))
            entries = res
        else:
            entries = parse_feed(raw)
    except Exception as e:
        return name, [], f"{name}: {type(e).__name__} {str(e)[:60]}"
    keep = [e for e in entries if e[2] is None or e[2] >= cutoff]
    keep.sort(key=lambda e: e[2] or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    items = []
    for title, link, d, summ in keep[:spec.get("max", per_feed)]:
        items.append({"outlet": name + (" (state media)" if spec.get("state_media") else ""), "region": spec.get("region", ""), "title": clean(title, 160), "url": link, "published": d.isoformat() if d else None, "summary": clean(summ, 200)})
    return name, items, (None if entries else f"{name}: no entries parsed")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--feeds", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--hours", type=int, default=36); ap.add_argument("--per-feed", type=int, default=12)
    a = ap.parse_args()
    feeds = json.load(open(a.feeds))
    cutoff = datetime.now(timezone.utc) - timedelta(hours=a.hours)
    all_items, failed, ok = [], [], 0
    with ThreadPoolExecutor(max_workers=16) as ex:
        for name, items, err in ex.map(lambda s: do_feed(s, cutoff, a.per_feed), feeds):
            if err: failed.append(err)
            if items: ok += 1
            all_items.extend(items)
    seen, uniq = set(), []
    for it in all_items:
        if it["url"] in seen: continue
        seen.add(it["url"]); uniq.append(it)
    for i, it in enumerate(uniq, 1): it["id"] = i
    json.dump({"generated": datetime.now(timezone.utc).isoformat(), "window_hours": a.hours, "items": uniq}, open(a.out, "w"), ensure_ascii=False)
    print(f"feeds with items: {ok}/{len(feeds)}; items: {len(uniq)}; failed or empty: {len(failed)}")
    for f in failed: print("  FAILED", f)

if __name__ == "__main__":
    main()

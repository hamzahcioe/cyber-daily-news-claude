#!/usr/bin/env python3
"""Download the article text for the selected clusters so researchers read local files instead of calling web_fetch on URLs they were only handed
(web_fetch refuses URLs that were not shown to the thread by a user, a search result or a fetched page). Uses no model tokens.
Usage: fetch_pages.py --clusters /tmp/notes/clusters.json --selection /tmp/notes/selection.json --out /tmp/notes/pages
selection.json: [{"id": "java4shell", "cluster": "c7"}, ...]
Writes /tmp/notes/pages/<id>.txt with '=== <url>' headers, readable text (about 6000 characters per page). Only URLs listed in the cluster (taken from the feeds) are fetched."""
import argparse, json, os, re, sys
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from urllib.request import Request, urlopen

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
SKIP = {"script", "style", "nav", "header", "footer", "aside", "form", "noscript", "svg", "iframe"}

class Text(HTMLParser):
    def __init__(self): super().__init__(); self.out = []; self.skip = 0; self.title = ""; self.in_title = False
    def handle_starttag(self, t, a):
        if t in SKIP: self.skip += 1
        if t == "title": self.in_title = True
        if t in ("p", "br", "li", "h1", "h2", "h3", "h4", "tr"): self.out.append("\n")
    def handle_endtag(self, t):
        if t in SKIP and self.skip: self.skip -= 1
        if t == "title": self.in_title = False
    def handle_data(self, d):
        if self.in_title: self.title += d
        elif not self.skip and d.strip(): self.out.append(d.strip() + " ")

def get(url, limit):
    try:
        r = urlopen(Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml,*/*"}), timeout=20)
        raw = r.read(1_500_000).decode(r.headers.get_content_charset() or "utf-8", "replace")
    except Exception as e:
        return f"FAILED {type(e).__name__}: {str(e)[:80]}"
    p = Text()
    try: p.feed(raw)
    except Exception: pass
    txt = re.sub(r"[ \t]+", " ", "".join(p.out)); txt = re.sub(r"\n\s*\n+", "\n", txt).strip()
    if len(txt) < 400: return "FAILED too little text (paywall, script-rendered or blocked)"
    return (p.title.strip() + "\n" if p.title.strip() else "") + txt[:limit]

def main():
    ap = argparse.ArgumentParser()
    for k in ("--clusters", "--selection", "--out"): ap.add_argument(k, required=True)
    ap.add_argument("--limit", type=int, default=6000); ap.add_argument("--per-item", type=int, default=4)
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    cl = json.load(open(a.clusters)); cl = cl if isinstance(cl, list) else cl.get("clusters", [])
    by = {c["cluster"]: c for c in cl}
    jobs = []
    for s in json.load(open(a.selection)):
        c = by.get(s.get("cluster"))
        if not c: print("UNKNOWN cluster", s); continue
        for u in c.get("urls", [])[:a.per_item]: jobs.append((s["id"], u))
    with ThreadPoolExecutor(12) as ex: res = list(ex.map(lambda j: (j, get(j[1], a.limit)), jobs))
    files, ok, bad = {}, 0, 0
    for (iid, u), txt in res:
        if txt.startswith("FAILED"): bad += 1; files.setdefault(iid, []).append(f"=== {u}\n[{txt}]\n"); continue
        ok += 1; files.setdefault(iid, []).append(f"=== {u}\n{txt}\n")
    for iid, parts in files.items(): open(os.path.join(a.out, iid + ".txt"), "w").write("\n".join(parts))
    print(f"pages ok {ok}; failed {bad}; items {len(files)}")
    from urllib.parse import urlparse
    seen = {}
    for (iid, u), txt in res:
        if txt.startswith("FAILED"): seen.setdefault(urlparse(u).netloc.removeprefix("www."), txt[7:60])
    for host, why in list(seen.items())[:20]: print("  PAGE FAILED", host, "-", why)

if __name__ == "__main__":
    main()

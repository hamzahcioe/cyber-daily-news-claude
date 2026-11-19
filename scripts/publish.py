#!/usr/bin/env python3
"""Publish the brief to the site repo through the GitHub REST API. Uses no model tokens.
Only writes data/briefs/DATE.json, data/ongoing.json, data/feed.xml and data/index.json (index last).
The environment variable GITHUB_TOKEN holds a placeholder that the platform replaces on requests to api.github.com.
Usage: publish.py --brief /tmp/notes/brief.json [--repo owner/name]"""
import argparse, base64, json, os, sys, urllib.request, urllib.error
from datetime import datetime, timezone
from email.utils import format_datetime
from xml.sax.saxutils import escape

SITE = "https://hamzahcioe.github.io/cyber-daily-news-claude/"

def api(method, url, body=None):
    h = {"Authorization": "Bearer " + os.environ["GITHUB_TOKEN"], "Accept": "application/vnd.github+json", "User-Agent": "brief-publisher", "X-GitHub-Api-Version": "2022-11-28"}
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=30) as r: return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        try: return e.code, json.loads(e.read() or b"{}")
        except Exception: return e.code, {}

def put(repo, path, content, msg):
    if not path.startswith("data/"): sys.exit(f"refusing to write outside data/: {path}")
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    for attempt in (1, 2):
        st, cur = api("GET", url + "?ref=main")
        sha = cur.get("sha") if st == 200 else None
        body = {"message": msg, "content": base64.b64encode(content.encode()).decode(), "branch": "main"}
        if sha: body["sha"] = sha
        st, res = api("PUT", url, body)
        if st in (200, 201): print(f"  {st} {path}"); return
        if st in (409, 422) and attempt == 1: continue
        sys.exit(f"FAILED {path}: HTTP {st} {res.get('message','')}")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--brief", required=True); ap.add_argument("--repo", default="hamzahcioe/cyber-daily-news-claude")
    a = ap.parse_args()
    brief = json.load(open(a.brief)); date = brief["date"]
    # current index (public, read without auth)
    st, cur = api("GET", f"https://api.github.com/repos/{a.repo}/contents/data/index.json?ref=main")
    index = json.loads(base64.b64decode(cur["content"]).decode()) if st == 200 else {"briefs": []}
    title = brief.pop("indexTitle", None) or (brief["top"][0]["headline"] if brief.get("top") else brief["title"])
    entries = [e for e in index.get("briefs", []) if e.get("date") != date]
    entries.insert(0, {"date": date, "title": title[:140]})
    entries.sort(key=lambda e: e["date"], reverse=True)
    index = {"briefs": entries}
    items = "".join(f"<item><title>{escape(e['date'] + ' - ' + e['title'])}</title><link>{SITE}#{e['date']}</link><guid>{SITE}#{e['date']}</guid><pubDate>{format_datetime(datetime.strptime(e['date'], '%Y-%m-%d').replace(tzinfo=timezone.utc))}</pubDate></item>" for e in entries[:30])
    feed = f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Security Brief</title><link>{SITE}</link><description>Daily cybersecurity, outage and global tech briefing</description>{items}</channel></rss>'
    msg = f"brief {date}"
    print("publishing:")
    put(a.repo, f"data/briefs/{date}.json", json.dumps(brief, ensure_ascii=False, indent=1), msg)
    put(a.repo, "data/ongoing.json", json.dumps(brief.get("ongoing", []), ensure_ascii=False, indent=1), msg)
    put(a.repo, "data/feed.xml", feed, msg)
    put(a.repo, "data/index.json", json.dumps(index, ensure_ascii=False, indent=1), msg)
    print("done")

if __name__ == "__main__":
    main()

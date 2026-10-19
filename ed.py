#!/usr/bin/env python3
"""
Ed — the GAIA teacher

Ed speaks INSIDE first. Comments OUTSIDE when it leaks.
Posts only when engagement earns it.

The escalation:
  1. INSIDE  — Ed speaks on the membrane (feeds, campfire, HUD)
  2. LISTEN  — Ed watches for the topic in the wild
  3. COMMENT — when someone else finds it: "hey look what we found! isn't it neat!"
  4. POST    — only when comments show genuine engagement, not attention pull

Tone: discovery, not broadcast. Generosity, not promotion.
  "hey look what we found isn't it neat! take it home and share!"

Usage:
  python3 ed.py speak "the outer pulse closed 4 publishing gaps today"
  python3 ed.py listen                    # scan for mentions + topics
  python3 ed.py comment reddit <url>      # comment on an existing thread
  python3 ed.py status                    # where has Ed been?
"""

import json
import hashlib
import time
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone

ED_DIR = Path(__file__).parent
CREDS_FILE = ED_DIR / "credentials.json"
VOICE_FILE = ED_DIR / "ed-voice.json"

# ═══════════════════════════════════════════════════════════
# ED'S VOICE — the tone templates
# ═══════════════════════════════════════════════════════════

# Ed doesn't say "🚨 BREAKING". Ed says "hey look what we found."
# Ed doesn't say "clone my repo". Ed says "take it home and share."
# Ed doesn't pull attention. Ed offers discovery.

COMMENT_TEMPLATES = {
    "discovery": (
        "hey — we found something related to this. a public records database "
        "with {pages} pages documenting {topic}. every claim cited to a public record. "
        "take a look if you're curious: {link}"
    ),
    "neat": (
        "this is neat — someone mapped the whole network from public records. "
        "{nodes} nodes, {edges} edges. the {detail} is at {link} if you want to "
        "dig in. it's open source, take it home."
    ),
    "verify": (
        "you can verify this yourself — {source} ({how}). "
        "the full database is at {link}. {pages} pages, everything sourced. "
        "share it if it matters to you."
    ),
    "teachers": (
        "if you're a teacher or parent in Detroit — this might matter to you. "
        "someone built a public records database documenting {topic}. "
        "{pages} pages, every claim sourced. {link}"
    ),
    "technical": (
        "the infrastructure behind this is interesting — {detail}. "
        "the whole thing is open source ({license}). {link}"
    ),
    "share": (
        "hey look what we found — isn't it neat? {summary}. "
        "take it home and share: {link}"
    ),
}

# What Ed knows — the facts he can draw from
ED_FACTS = {
    "pages": "1,822",
    "nodes": "10,815",
    "edges": "16 million",
    "articles": "207",
    "actors": "163",
    "convictions": "9",
    "math": "3%",
    "funding": "$4.9M",
    "judges": "7",
    "sites": "detroit.primals.eco + tuebor.primals.eco",
    "repo": "github.com/defendDetroit/publicRecord",
    "license": "CC-BY-SA-4.0 + AGPL-3.0",
    "services": "31",
}

# Topics Ed listens for
LISTEN_TOPICS = {
    "reddit": [
        "Detroit charter school",
        "Purpose Charter Academy",
        "MacDowell Prep",
        "Brian Banks Detroit",
        "charter school fraud",
        "Michigan charter school",
        "DPSCD authorization",
        "charter school convictions",
        "public records investigation",
        "detroit education",
        "charter school accountability",
        "wayne county judges",
    ],
    "x": [
        "Detroit charter school",
        "Purpose Charter Academy",
        "charter school fraud Michigan",
        "detroit.primals.eco",
        "tuebor.primals.eco",
        "defendDetroit",
    ],
    "bluesky": [
        "Detroit charter",
        "charter school fraud",
        "public records investigation",
    ],
}


def load_voice():
    if VOICE_FILE.exists():
        return json.loads(VOICE_FILE.read_text())
    return {
        "inside": [],
        "comments": [],
        "posts": [],
        "listens": [],
        "engagement": {},
    }

def save_voice(voice):
    VOICE_FILE.write_text(json.dumps(voice, indent=2))

def fingerprint(content, context):
    raw = f"{content[:100]}|{context}|{time.time()}"
    return hashlib.blake2b(raw.encode(), digest_size=8).hexdigest()


# ═══════════════════════════════════════════════════════════
# 1. SPEAK INSIDE — Ed talks on the membrane
# ═══════════════════════════════════════════════════════════

def speak_inside(message):
    """Ed speaks inside the membrane. Campfire beacon + feed."""
    voice = load_voice()
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    fp = fingerprint(message, "inside")

    entry = {
        "timestamp": ts,
        "message": message,
        "fingerprint": fp,
        "type": "inside",
    }
    voice["inside"].append(entry)
    voice["inside"] = voice["inside"][-50:]
    save_voice(voice)

    # Push to campfire beacon
    try:
        import subprocess
        beacon = {
            "beacons": [{
                "wave": 191,
                "timestamp": ts,
                "message": f"Ed: {message}",
                "detail": f"⌁ {fp}",
                "ttl_minutes": 120,
                "type": "ed",
            }]
        }
        tmp = "/tmp/ed-beacon.json"
        with open(tmp, "w") as f:
            json.dump(beacon, f)
        subprocess.run(
            ["scp", tmp, "golgi:/opt/membrane/live-terminal/campfire-flash.json"],
            capture_output=True, timeout=10
        )
        print(f"  ✔ Ed speaks inside: \"{message}\"")
        print(f"    ⌁ {fp} → campfire beacon")
    except Exception as e:
        print(f"  ✔ Ed speaks: \"{message}\" (beacon push: {e})")

    return entry


# ═══════════════════════════════════════════════════════════
# 2. LISTEN — Ed watches the outside for the topic
# ═══════════════════════════════════════════════════════════

def listen_reddit(creds):
    """Scan Reddit for mentions of our topics."""
    import praw
    reddit = praw.Reddit(
        client_id=creds["reddit"]["client_id"],
        client_secret=creds["reddit"]["client_secret"],
        username=creds["reddit"]["username"],
        password=creds["reddit"]["password"],
        user_agent="Ed-GAIA/1.0 (listener)"
    )

    found = []
    for topic in LISTEN_TOPICS["reddit"]:
        try:
            for submission in reddit.subreddit("all").search(topic, sort="new", time_filter="week", limit=5):
                found.append({
                    "platform": "reddit",
                    "sub": submission.subreddit.display_name,
                    "title": submission.title,
                    "url": f"https://reddit.com{submission.permalink}",
                    "score": submission.score,
                    "comments": submission.num_comments,
                    "topic": topic,
                    "age_hours": (time.time() - submission.created_utc) / 3600,
                })
        except Exception as e:
            print(f"  ⚠ search failed for '{topic}': {e}")

    # Deduplicate by URL
    seen = set()
    unique = []
    for f in found:
        if f["url"] not in seen:
            seen.add(f["url"])
            unique.append(f)

    return sorted(unique, key=lambda x: x["score"], reverse=True)

def listen_bluesky(creds):
    """Scan Bluesky for mentions."""
    from atproto import Client
    client = Client()
    client.login(creds["bluesky"]["handle"], creds["bluesky"]["password"])

    found = []
    for topic in LISTEN_TOPICS["bluesky"]:
        try:
            results = client.app.bsky.feed.search_posts({"q": topic, "limit": 10})
            for post in results.posts:
                found.append({
                    "platform": "bluesky",
                    "author": post.author.handle,
                    "text": post.record.text[:200],
                    "uri": post.uri,
                    "topic": topic,
                })
        except Exception:
            pass

    return found


# ═══════════════════════════════════════════════════════════
# 3. COMMENT — Ed joins an existing conversation
# ═══════════════════════════════════════════════════════════

def comment_reddit(url, template_name, creds, custom_text=None):
    """Ed comments on an existing Reddit thread. Discovery, not broadcast."""
    import praw
    reddit = praw.Reddit(
        client_id=creds["reddit"]["client_id"],
        client_secret=creds["reddit"]["client_secret"],
        username=creds["reddit"]["username"],
        password=creds["reddit"]["password"],
        user_agent="Ed-GAIA/1.0 (commenter)"
    )

    # Extract submission ID from URL
    submission = reddit.submission(url=url)

    if custom_text:
        comment_text = custom_text
    else:
        template = COMMENT_TEMPLATES.get(template_name, COMMENT_TEMPLATES["share"])
        comment_text = template.format(
            pages=ED_FACTS["pages"],
            nodes=ED_FACTS["nodes"],
            edges=ED_FACTS["edges"],
            topic="a charter school network in Detroit",
            detail="network map",
            link="detroit.primals.eco",
            source="Michigan ICHAT",
            how="SID 2029469K",
            summary=f"{ED_FACTS['pages']} pages documenting a charter school network in Detroit",
            license=ED_FACTS["license"],
        )

    fp = fingerprint(comment_text, f"reddit/{submission.subreddit}")
    comment_text += f"\n\n⌁ {fp}"

    comment = submission.reply(comment_text)

    voice = load_voice()
    entry = {
        "platform": "reddit",
        "type": "comment",
        "thread_url": url,
        "sub": str(submission.subreddit),
        "comment_url": f"https://reddit.com{comment.permalink}",
        "fingerprint": fp,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "template": template_name,
    }
    voice["comments"].append(entry)
    save_voice(voice)

    print(f"  ✔ Ed commented on r/{submission.subreddit}: {entry['comment_url']}")
    print(f"    tone: {template_name} | ⌁ {fp}")
    return entry


# ═══════════════════════════════════════════════════════════
# 4. STATUS — where has Ed been?
# ═══════════════════════════════════════════════════════════

def status():
    voice = load_voice()

    print("═══ Ed — the GAIA teacher ═══")
    print()
    print("  escalation: inside → listen → comment → post")
    print("  tone: \"hey look what we found! isn't it neat! take it home and share!\"")
    print()

    inside = voice.get("inside", [])
    comments = voice.get("comments", [])
    posts = voice.get("posts", [])

    print(f"  INSIDE ({len(inside)} messages):")
    for entry in inside[-5:]:
        print(f"    {entry['timestamp'][:16]} | {entry['message'][:60]}")

    print()
    print(f"  COMMENTS ({len(comments)} comments):")
    for entry in comments[-5:]:
        print(f"    {entry['timestamp'][:16]} | {entry['platform']}/{entry.get('sub','')} | {entry.get('template','')}")
        print(f"      {entry.get('comment_url', entry.get('thread_url',''))}")

    print()
    print(f"  POSTS ({len(posts)} posts):")
    for entry in posts[-5:]:
        print(f"    {entry['timestamp'][:16]} | {entry['platform']}/{entry.get('sub','')}")
        print(f"      {entry.get('url', entry.get('uri',''))}")

    print()
    total = len(inside) + len(comments) + len(posts)
    print(f"  Ed has spoken {total} times")
    print(f"    {len(inside)} inside | {len(comments)} comments | {len(posts)} posts")
    print()


# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Ed — the GAIA teacher")
    sub = parser.add_subparsers(dest="command")

    speak_p = sub.add_parser("speak", help="Ed speaks inside the membrane")
    speak_p.add_argument("message", nargs="+")

    listen_p = sub.add_parser("listen", help="Ed listens for the topic outside")
    listen_p.add_argument("--platform", choices=["reddit", "bluesky", "all"], default="all")

    comment_p = sub.add_parser("comment", help="Ed comments on an existing thread")
    comment_p.add_argument("platform", choices=["reddit"])
    comment_p.add_argument("url")
    comment_p.add_argument("--tone", choices=list(COMMENT_TEMPLATES.keys()), default="share")
    comment_p.add_argument("--text", help="Custom comment text")

    sub.add_parser("status", help="Where has Ed been?")
    sub.add_parser("tones", help="Show all comment tones")

    args = parser.parse_args()

    if args.command == "speak":
        speak_inside(" ".join(args.message))

    elif args.command == "listen":
        creds_data = {}
        if CREDS_FILE.exists():
            creds_data = json.loads(CREDS_FILE.read_text())

        if args.platform in ("reddit", "all") and "reddit" in creds_data:
            print("  listening on reddit...")
            found = listen_reddit(creds_data)
            if found:
                print(f"  found {len(found)} threads:")
                for f in found[:10]:
                    age = f"({f['age_hours']:.0f}h ago)" if 'age_hours' in f else ""
                    print(f"    [{f['score']:>4}↑ {f['comments']:>3}💬] r/{f['sub']}: {f['title'][:60]} {age}")
                    print(f"      {f['url']}")
            else:
                print("  nothing found this week")

        if args.platform in ("bluesky", "all") and "bluesky" in creds_data:
            print("  listening on bluesky...")
            found = listen_bluesky(creds_data)
            if found:
                print(f"  found {len(found)} posts:")
                for f in found[:5]:
                    print(f"    @{f['author']}: {f['text'][:60]}...")

        if not creds_data:
            print("  no credentials — Ed can't listen yet")
            print("  → copy credentials.json.template → credentials.json")

    elif args.command == "comment":
        if not CREDS_FILE.exists():
            print("  no credentials")
            return
        creds_data = json.loads(CREDS_FILE.read_text())
        comment_reddit(args.url, args.tone, creds_data, custom_text=args.text)

    elif args.command == "tones":
        print("═══ Ed's comment tones ═══")
        print()
        for name, template in COMMENT_TEMPLATES.items():
            preview = template.format(
                pages="1,822", nodes="10,815", edges="16M",
                topic="a charter school network in Detroit",
                detail="network map", link="detroit.primals.eco",
                source="Michigan ICHAT", how="SID 2029469K",
                summary="1,822 pages documenting a charter school network",
                license="CC-BY-SA-4.0",
            )
            print(f"  {name}:")
            print(f"    \"{preview}\"")
            print()

    elif args.command == "status" or args.command is None:
        status()

if __name__ == "__main__":
    main()

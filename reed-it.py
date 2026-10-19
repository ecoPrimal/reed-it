#!/usr/bin/env python3
"""
rEEd it — social membrane broadcaster
Ed the GAIA teacher speaks. Proof of first. Grows the mesh.

Each platform maps to a membrane primal:

    Platform        Symbol    Primal            Guide
    ────────        ──────    ──────            ─────
    X/Twitter       × # @    epitope           sort by tag, cross-ref, address
    Reddit          ↑↓ r/    scan_sweep_sort   upvote=commensal, downvote=null
    Bluesky         AT://    beardog           sovereign identity, self-hosted keys
    Mastodon        🐘 AP    plasmid           federated, ActivityPub = plasmid exchange
    LinkedIn        🔗 CV    krogan            trust grading, credential verification
    Threads         🧵       pollination       cross-pollination into walled garden
    HackerNews      Y        architecture      first-principles, technical mesh
    Instagram       📷       sporeprint        visual imprint — image IS evidence
    Substack        📝       tuebor            long-form analysis surface
    Tumblr          t        hypothesis        questions, reblog = signal propagation

Each post:
  1. Fires content to the platform
  2. Immediately posts a minimal first-comment (proof of origin)
  3. Records the post URL + timestamp in the membrane feed
  4. Returns proof to the membrane — grows the mesh

The first comment is SMALL — a membrane fingerprint, not a wall of text.
It proves you were first. It doesn't bloat the thread.

Usage:
  python3 reed-it.py --platform all --dry-run
  python3 reed-it.py --platform x
  python3 reed-it.py --platform reddit --sub Detroit
  python3 reed-it.py --platform bluesky
  python3 reed-it.py --platform mastodon
  python3 reed-it.py --platform all
  python3 reed-it.py --status
"""

import json
import hashlib
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone

REED_DIR = Path(__file__).parent
CREDS_FILE = REED_DIR / "credentials.json"
PROOF_FILE = REED_DIR / "proof-of-first.json"
POSTS_DIR = REED_DIR / "posts"

# ═══════════════════════════════════════════════════════════
# PRIMAL MAP — each platform has a membrane guide
# ═══════════════════════════════════════════════════════════

PRIMALS = {
    "x":          {"symbol": "× # @",  "primal": "epitope",         "guide": "sort by tag, cross-ref, address"},
    "reddit":     {"symbol": "↑↓ r/",  "primal": "scan_sweep_sort", "guide": "upvote=commensal, downvote=null"},
    "bluesky":    {"symbol": "AT://",  "primal": "beardog",         "guide": "sovereign identity, self-hosted keys"},
    "mastodon":   {"symbol": "🐘 AP",  "primal": "plasmid",         "guide": "federated, ActivityPub = plasmid exchange"},
    "linkedin":   {"symbol": "🔗 CV",  "primal": "krogan",          "guide": "trust grading, credential verification"},
    "threads":    {"symbol": "🧵",     "primal": "pollination",     "guide": "cross-pollination into walled garden"},
    "hackernews": {"symbol": "Y",      "primal": "architecture",    "guide": "first-principles, technical mesh"},
    "instagram":  {"symbol": "📷",     "primal": "sporeprint",      "guide": "visual imprint — image IS evidence"},
    "substack":   {"symbol": "📝",     "primal": "tuebor",          "guide": "long-form analysis surface"},
    "tumblr":     {"symbol": "t",      "primal": "hypothesis",      "guide": "questions, reblog = signal propagation"},
}

def load_creds():
    if CREDS_FILE.exists():
        return json.loads(CREDS_FILE.read_text())
    return {}

def load_proof():
    if PROOF_FILE.exists():
        return json.loads(PROOF_FILE.read_text())
    return {"posts": [], "first_comments": []}

def save_proof(proof):
    PROOF_FILE.write_text(json.dumps(proof, indent=2))

def membrane_fingerprint(content, platform, ts):
    raw = f"{content[:100]}|{platform}|{ts}"
    return hashlib.blake2b(raw.encode(), digest_size=8).hexdigest()

def first_comment_text(fingerprint):
    return (
        f"⌁ {fingerprint}\n"
        f"detroit.primals.eco — public record, git-verified\n"
        f"verify: tuebor.primals.eco/analysis/the-desk-in-the-mountains/"
    )

def record_proof(result, proof):
    if result:
        proof["posts"].append(result)
        save_proof(proof)

def push_proof_to_membrane(proof):
    try:
        import subprocess
        tmp = "/tmp/reed-it-proof.json"
        with open(tmp, "w") as f:
            json.dump(proof, f, indent=2)
        subprocess.run(
            ["scp", tmp, "golgi:/opt/membrane/live-terminal/reed-it-proof.json"],
            capture_output=True, timeout=10
        )
        print("  ✔ proof pushed to membrane")
    except Exception as e:
        print(f"  ✘ membrane push failed: {e}")


# ═══════════════════════════════════════════════════════════
# X / TWITTER — epitope (× # @)
# ═══════════════════════════════════════════════════════════

X_THREAD = [
    # Tweet 1 — The Hook
    (
        "🚨 9 criminal convictions. 3% math proficiency. $4.9M in public money.\n\n"
        "A man runs two Detroit charter schools. His response to a documented investigation? "
        "A restraining order — filed the same day the State Board of Education had the evidence.\n\n"
        "detroit.primals.eco 🧵"
    ),
    # Tweet 2 — The Facts
    (
        "Brian Banks — 9 convictions (6 felony). Claims a J.D. — zero results on the "
        "State Bar of Michigan.\n\n"
        "Runs Purpose Charter Academy + MacDowell Prep. Board chairs: two sitting Wayne County judges.\n\n"
        "1,822 pages. Every claim cited to public records. Verify on ICHAT (SID 2029469K)."
    ),
    # Tweet 3 — The Venue
    (
        "He filed the PPO in Wayne County — where he has 7 connected judges across 4 courts. "
        "Not in Ingham County where the respondent lives.\n\n"
        "Judge Yvonna Abraham signed it ex parte. Same day. No hearing.\n\n"
        "The respondent is now in LEIN — a law enforcement database — for filing FOIA requests."
    ),
    # Tweet 4 — The Channels
    (
        "22 channels contacted. 4 responded. 17 were silent. 1 retaliated.\n\n"
        "Federal referral packets sent to 8 agencies. Two civil actions filed. Service completed.\n\n"
        "Independently corroborated by Clutch Justice and Detroit Free Press / M.L. Elrick."
    ),
    # Tweet 5 — The Record
    (
        "The investigation is 1,822 pages across 2 sites. 10,815 nodes. 16 million edges. "
        "207 analysis articles. Git-verified. Open source.\n\n"
        "git clone https://github.com/defendDetroit/publicRecord.git\n\n"
        "If this signal goes dark, now you know why."
    ),
]

def post_x(creds):
    import tweepy

    client = tweepy.Client(
        consumer_key=creds["x"]["api_key"],
        consumer_secret=creds["x"]["api_secret"],
        access_token=creds["x"]["access_token"],
        access_token_secret=creds["x"]["access_token_secret"],
    )

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    results = []
    prev_id = None

    for i, tweet_text in enumerate(X_THREAD):
        resp = client.create_tweet(
            text=tweet_text,
            in_reply_to_tweet_id=prev_id
        )
        prev_id = resp.data["id"]
        tweet_url = f"https://x.com/i/status/{prev_id}"

        if i == 0:
            fp = membrane_fingerprint(tweet_text, "x", ts)
            proof_resp = client.create_tweet(
                text=first_comment_text(fp),
                in_reply_to_tweet_id=prev_id
            )

        results.append({"tweet": i + 1, "id": prev_id, "url": tweet_url})
        print(f"  ✔ tweet {i+1}/{len(X_THREAD)}: {tweet_url}")

    fp = membrane_fingerprint(X_THREAD[0], "x", ts)
    print(f"    first comment: ⌁ {fp}")

    return {
        "platform": "x",
        "thread": results,
        "url": results[0]["url"],
        "fingerprint": fp,
        "timestamp": ts,
    }


# ═══════════════════════════════════════════════════════════
# REDDIT — scan_sweep_sort (↑↓ r/)
# ═══════════════════════════════════════════════════════════

REDDIT_POSTS = {
    "Detroit": {
        "title": "I built a public records database documenting a Detroit charter school network. 1,822 pages, everything sourced.",
        "body": """I've been working on this for a while and finally feel like it's ready for people to see.

A man with 9 criminal convictions — including 6 felonies — has been running charter schools in Detroit for over a decade, receiving $4.9 million annually in public education funding. The authorizer, judges, and political figures around him form a network I've mapped entirely from public records.

The site is [detroit.primals.eco](https://detroit.primals.eco). Every claim links to its source — OTIS criminal records, LARA business filings, Wayne County property records, campaign finance disclosures, court dockets. There's a [site index](https://detroit.primals.eco/site-index/) if you want the full scope.

I'm not a journalist. I'm a data scientist who got pulled into this through a custody case. I built the investigation infrastructure myself because no one else was going to do it.

Two civil actions are filed. Federal referrals sent to eight agencies. The [evidence](https://detroit.primals.eco/evidence/) is all public.

If you know families affected by Purpose Charter Academy or MacDowell Prep, the [contact page](https://detroit.primals.eco/contact/) has information for them."""
    },
    "Teachers": {
        "title": "A Detroit charter school superintendent has 9 criminal convictions. His school's math proficiency is 3%. I documented the entire network from public records.",
        "body": """I know teachers on here have charter school horror stories. I want to share what I found when I started pulling public records on a Detroit charter network.

The superintendent of MacDowell Preparatory Academy has 9 criminal convictions (6 felonies) including larceny and financial crimes. His school reported 3% math proficiency. He receives $4.9M in annual public funding through a network of entities he controls.

He also claims a J.D. on his published book. The Michigan State Bar has zero results for his name.

I'm not a teacher — I'm a computational biologist who got dragged into this through a family court matter. I applied the same methodology I use for scientific research: primary sources, reproducible analysis, everything cited.

The result is a 1,822-page public records analysis across two sites: [detroit.primals.eco](https://detroit.primals.eco) and [tuebor.primals.eco](https://tuebor.primals.eco)

Pages that might interest teachers specifically:

- [The RICO pattern analysis](https://detroit.primals.eco/analysis/rico-pattern/) — how the money flows
- [Credential audit](https://detroit.primals.eco/analysis/credential-audit/) — the fake J.D. and what the State Bar shows
- [Institutional capture](https://detroit.primals.eco/analysis/institutional-capture/) — how one person captured schools, courts, and political offices

Every fact is cited to a public record you can verify yourself. The [Verify Everything](https://detroit.primals.eco/validate/) page walks you through it."""
    },
    "Michigan": {
        "title": "I filed complaints with the Michigan Department of Education about a charter school superintendent with 9 criminal convictions. Here's the 1,822-page public records database I built.",
        "body": """For the past several months I've been building a public records analysis of a Detroit charter school network. The superintendent has 9 criminal convictions including 6 felonies. His school receives $4.9M in annual state funding. Formal complaints are pending with MDE.

The full analysis is at [detroit.primals.eco](https://detroit.primals.eco) — 1,822 pages across two sites, every claim sourced to OTIS records, LARA filings, campaign finance disclosures, and court dockets.

I'm a Michigan State alum (BS Microbiology, MS Data Science) who built this because the public records tell a story that nobody was putting together. Two civil actions are filed in Ingham County. Federal referral packets have been sent to eight agencies.

The [site index](https://detroit.primals.eco/site-index/) has the full scope. The [evidence page](https://detroit.primals.eco/evidence/) has the documents."""
    },
    "education": {
        "title": "What happens when a charter school authorizer doesn't check criminal records? I documented one case from public records — 1,822 pages.",
        "body": """I spent several months building a public records database about a charter school network in Detroit. The question that kept coming up wasn't about one person — it was about the system that let it happen.

A superintendent with 9 criminal convictions (6 felonies including larceny) has been running publicly-funded schools for 14+ years. His school reports 3% math proficiency. He claims a J.D. on his published book — the Michigan State Bar returns zero results for his name.

I'm not an education policy expert. I'm a data scientist. I applied entity-relationship mapping and network analysis to public records — OTIS, LARA, campaign finance, property records, court dockets — and built a 1,822-page analysis: [detroit.primals.eco](https://detroit.primals.eco)

The analysis includes:
- A [RICO pattern analysis](https://detroit.primals.eco/analysis/rico-pattern/)
- A [network map](https://detroit.primals.eco/network/) showing connections between the superintendent, judges, political figures, and shell entities
- A [credential audit](https://detroit.primals.eco/analysis/credential-audit/)
- Step-by-step [verification instructions](https://detroit.primals.eco/validate/) so you can confirm everything independently

The broader question: if this can happen in plain sight in public records that anyone can access, what does that say about charter school oversight nationally?"""
    },
    "charterschools": {
        "title": "Public records analysis of a Detroit charter school network — 10,815 nodes, 16M edges, $4.9M annual funding, superintendent with 9 criminal convictions",
        "body": """I built a public records database documenting a charter school network in Detroit: [detroit.primals.eco](https://detroit.primals.eco)

The core finding: a superintendent with 9 criminal convictions (6 felonies) has been running publicly-funded charter schools for 14+ years, receiving $4.9M annually. The network includes shell entities, connected judges, campaign finance relationships, and a guardianship services company run by a non-attorney.

I'm not anti-charter. I'm a data scientist who believes accountability structures should work regardless of school type. The question this case raises is: what happens when the authorizer doesn't do its job?

The methodology is computational — entity-relationship mapping, network graph analysis, public records cross-referencing. Everything is sourced and independently verifiable. The entire codebase is in a [public git repository](https://git.primals.eco/publicRecord/detroit).

If anyone here works in charter school governance or oversight, I'd welcome feedback on the analysis."""
    },
    "publicinterest": {
        "title": "Pro se plaintiff built a 1,822-page public records analysis of charter school fraud in Detroit — looking for civil rights attorneys who want to carry the courtroom",
        "body": """Not seeking legal advice — sharing a case that might interest public interest attorneys.

I'm a pro se plaintiff with two civil actions filed in Ingham County Circuit Court (2026-4301-CZ, 2026-4349-CZ). Service completed, defaults approaching. Federal referral packets sent to eight agencies.

The underlying case: a charter school superintendent with 9 criminal convictions running $4.9M/year in publicly-funded schools in Detroit, connected to judges, political figures, and shell entities — all documented from public records.

I built the investigation database myself: [detroit.primals.eco](https://detroit.primals.eco). 1,822 pages, everything sourced. The full [contact page](https://detroit.primals.eco/contact/#for-attorneys) has details for attorneys.

I'm not interested in settlement. I want jury trial, accountability, and resignations."""
    },
    "dataisbeautiful": {
        "title": "[OC] Network graph of a Detroit charter school investigation: 10,815 nodes, 16 million edges, 9 judges across 4 courts",
        "body": """Entity-relationship graph built from public records documenting a charter school network in Detroit.

Data sources: OTIS criminal records, LARA business filings, campaign finance disclosures (MI SOS), Wayne County property records, court dockets across 4 courts.

10,815 nodes (entities: people, organizations, LLCs, courts, schools, campaign committees). 16 million edges (relationships: financial, governance, legal, political). Rendered with network analysis tools from public records cross-referencing.

Interactive version: [detroit.primals.eco/network/](https://detroit.primals.eco/network/)
Raw graph data: [detroit.primals.eco/graph.json](https://detroit.primals.eco/graph.json) (JSON), [detroit.primals.eco/graph.csv](https://detroit.primals.eco/graph.csv) (CSV for Gephi/pandas/R)

Tools: Zola static site generator, Python entity-relationship mapping, custom graph construction from public records APIs.

Source: [git.primals.eco/publicRecord/detroit](https://git.primals.eco/publicRecord/detroit)"""
    },
    "homelab": {
        "title": "31 services on a $6/mo VPS — sovereign investigation infrastructure with WireGuard mesh, Caddy, and a 2-minute heartbeat",
        "body": """I run a public records investigation from a 2GB VPS (golgi) meshed to a home lab via WireGuard.

The stack:
- **31 services** on a 1-core/2GB Debian VPS
- **WireGuard mesh**: 4 peers (golgi VPS, eastGate workstation, northGate laptop, sporeGate build server)
- **Caddy**: reverse proxy for 9 public sites (tuebor, detroit, sporeprint, hypothesis, thesis, signal, hud, mesh, pollination)
- **Custom Python pipeline** (membrane-pulse): heartbeat every 2 minutes — pulls from git, builds Zola sites, deploys, runs security scans
- **Songbird**: challenge server (ports 7700/7780/8091)
- **beardog**: security gatekeeper — classifies all traffic into 5 trust tiers
- **13 JSON feeds**: live membrane data (scan, engagement, dynamics, architecture, etc.)
- **17 QR codes**: generated for every human entry point

The investigation it serves: 1,822 pages documenting a charter school network in Detroit. 10,815 nodes, 16 million edges. Every claim cited to public records.

Sites: detroit.primals.eco + tuebor.primals.eco
Repo: github.com/defendDetroit/publicRecord

The whole thing runs on 2GB RAM. Zola builds take 45-60 seconds. The heartbeat monitors, rebuilds, and deploys without human intervention.

Happy to answer questions about the architecture."""
    },
}

def post_reddit(sub_name, creds):
    import praw
    reddit = praw.Reddit(
        client_id=creds["reddit"]["client_id"],
        client_secret=creds["reddit"]["client_secret"],
        username=creds["reddit"]["username"],
        password=creds["reddit"]["password"],
        user_agent="rEEd-it/1.0 (by Ed the GAIA teacher)"
    )
    if sub_name not in REDDIT_POSTS:
        print(f"  ✘ no post drafted for r/{sub_name}")
        return None
    post_data = REDDIT_POSTS[sub_name]
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    subreddit = reddit.subreddit(sub_name)
    submission = subreddit.submit(title=post_data["title"], selftext=post_data["body"])
    fp = membrane_fingerprint(post_data["body"], f"reddit/{sub_name}", ts)
    comment = submission.reply(first_comment_text(fp))
    result = {
        "platform": "reddit", "sub": sub_name,
        "url": f"https://reddit.com{submission.permalink}",
        "comment_url": f"https://reddit.com{comment.permalink}" if comment else None,
        "fingerprint": fp, "timestamp": ts, "title": post_data["title"],
    }
    print(f"  ✔ r/{sub_name}: {result['url']}")
    print(f"    ⌁ {fp}")
    return result


# ═══════════════════════════════════════════════════════════
# BLUESKY — beardog (AT://)
# ═══════════════════════════════════════════════════════════

BLUESKY_POST = (
    "A man with 9 criminal convictions runs Detroit charter schools with 3% math proficiency. "
    "$4.9M in public money. 72.67% extracted to his private LLC.\n\n"
    "He responded to a documented investigation with a restraining order — "
    "filed the same day the State Board of Education had the evidence.\n\n"
    "1,822 pages. Git-verified. Open source.\n\n"
    "detroit.primals.eco"
)

def post_bluesky(creds):
    from atproto import Client
    client = Client()
    client.login(creds["bluesky"]["handle"], creds["bluesky"]["password"])
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    fp = membrane_fingerprint(BLUESKY_POST, "bluesky", ts)
    post = client.send_post(text=BLUESKY_POST)
    client.send_post(text=first_comment_text(fp), reply_to={"root": post, "parent": post})
    result = {
        "platform": "bluesky", "uri": post.uri, "cid": post.cid,
        "fingerprint": fp, "timestamp": ts,
    }
    print(f"  ✔ bluesky: {post.uri}")
    print(f"    ⌁ {fp}")
    return result


# ═══════════════════════════════════════════════════════════
# MASTODON — plasmid (🐘 AP)
# ═══════════════════════════════════════════════════════════

MASTODON_POST = (
    "🚨 A charter school operator with 9 criminal convictions filed a restraining order "
    "against the person who documented his record.\n\n"
    "3% math proficiency. $4.9M in public money. 7 connected judges across 4 courts. "
    "Two sitting judges chair his school boards.\n\n"
    "1,822 pages of evidence. Every claim cites public records. Git-verified. Open source.\n\n"
    "detroit.primals.eco\n\n"
    "#Detroit #CharterSchools #OpenData #PublicRecords #Accountability "
    "#Education #FOIA #Michigan #RICO #OpenSource #PublicSchools "
    "#DataScience #Transparency"
)

def post_mastodon(creds):
    from mastodon import Mastodon
    api = Mastodon(
        access_token=creds["mastodon"]["access_token"],
        api_base_url=creds["mastodon"]["instance_url"]
    )
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    fp = membrane_fingerprint(MASTODON_POST, "mastodon", ts)
    status = api.status_post(MASTODON_POST)
    api.status_reply(status, first_comment_text(fp))
    result = {
        "platform": "mastodon", "url": status["url"], "id": status["id"],
        "fingerprint": fp, "timestamp": ts,
    }
    print(f"  ✔ mastodon: {result['url']}")
    print(f"    ⌁ {fp}")
    return result


# ═══════════════════════════════════════════════════════════
# MANUAL PLATFORMS — text saved to posts/ for copy-paste
# ═══════════════════════════════════════════════════════════

MANUAL_POSTS = {
    "linkedin": {
        "primal": "krogan",
        "text": (
            "I spent 5 years as a Clerical Technical Union member at Michigan State University. "
            "During that time I learned what institutional accountability looks like — and what it "
            "looks like when institutions fail.\n\n"
            "Today I'm publishing a public evidence library documenting a pattern I believe constitutes "
            "racketeering in Detroit charter schools.\n\n"
            "The superintendent has 9 criminal convictions including 6 felonies. His school reports "
            "3% math proficiency. He receives $4.9M in annual public funding. 72.67% of revenue flows "
            "to his private management company.\n\n"
            "His response to a documented investigation? Not a correction. Not a defamation claim. "
            "A restraining order — filed the same day the State Board of Education had the evidence package.\n\n"
            "The investigation is 1,822 pages across two sites. 10,815 nodes. 16 million edges. "
            "207 analysis articles. Every claim is cited to public records. Every document is "
            "git-verified and timestamped.\n\n"
            "The investigation is open source: detroit.primals.eco\n\n"
            "If you work in education, law, public policy, data science, or journalism — "
            "the evidence is there. Verify it yourself.\n\n"
            "#Education #PublicPolicy #DataScience #Accountability #Detroit #Michigan #OpenSource #CharterSchools"
        ),
    },
    "threads": {
        "primal": "pollination",
        "text": (
            "A man with 9 criminal convictions runs charter schools in Detroit. "
            "3% math proficiency. $4.9M in public funding.\n\n"
            "He filed a restraining order against the person who documented it — "
            "the same day the State Board of Education had the evidence.\n\n"
            "1,822 pages. Every fact cited to public records. Open source.\n\n"
            "detroit.primals.eco"
        ),
    },
    "hackernews": {
        "primal": "architecture",
        "title": "Show HN: Git-verified open-source investigation — 1,822 pages, 10,815 nodes, 16M edges",
        "text": (
            "I built an open-source public records investigation as a pair of Zola static sites "
            "served from a 2GB VPS.\n\n"
            "The investigation documents a charter school network in Detroit — a superintendent "
            "with 9 criminal convictions running $4.9M/year in publicly-funded schools, connected "
            "to judges and political figures.\n\n"
            "The technical infrastructure:\n"
            "- 2 Zola static sites: 1,822 pages total (1,199 tuebor + 623 detroit)\n"
            "- Git-verified: every page committed, timestamped, BLAKE3-hashed\n"
            "- Network graph: 10,815 nodes, 16M edges\n"
            "- 31 services on a membrane architecture (WireGuard mesh, Caddy, custom Python pipeline)\n"
            "- Structured data: JSON-LD on every page, llms.txt, sitemap, content manifest\n"
            "- 100% open: robots.txt allows all crawlers, AI agents, archives\n"
            "- License: CC-BY-SA-4.0 (content), AGPL-3.0 (code)\n\n"
            "Sites: detroit.primals.eco (evidence) and tuebor.primals.eco (analysis)\n"
            "Repo: github.com/defendDetroit/publicRecord\n\n"
            "What I'd like feedback on: the entity-relationship methodology and whether this kind of "
            "structured public records work has legs as a reproducible framework."
        ),
    },
    "instagram": {
        "primal": "sporeprint",
        "text": (
            "9 convictions. 3% math. $4.9M public money. 7 connected judges.\n\n"
            "A charter school operator filed a restraining order against the person "
            "who documented his public record.\n\n"
            "1,822 pages of evidence. Every fact sourced. Git-verified. Open source.\n\n"
            "Link in bio: detroit.primals.eco\n\n"
            "#Detroit #CharterSchools #PublicRecords #Accountability #Education "
            "#Michigan #OpenData #FOIA #DataScience #OpenSource"
        ),
    },
    "tumblr": {
        "primal": "hypothesis",
        "title": "What happens when a charter school authorizer doesn't check criminal records?",
        "text": (
            "A superintendent with 9 criminal convictions — including 6 felonies — "
            "has been running publicly-funded charter schools in Detroit for over a decade.\n\n"
            "3% math proficiency. $4.9M in annual public funding. Two sitting judges chair his school boards.\n\n"
            "He responded to a documented investigation with a restraining order — "
            "filed the same day the State Board of Education had the evidence.\n\n"
            "I'm not a journalist. I'm a data scientist who built a 1,822-page public records database "
            "because nobody else was going to.\n\n"
            "detroit.primals.eco\n\n"
            "Every claim is cited to a public record you can verify yourself. "
            "Clone the repo. Check the sources. Share the signal."
        ),
    },
    "substack": {
        "primal": "tuebor",
        "title": "The Desk in the Mountains — How a Living System Watches Over Public Money",
        "text": (
            "The full article is live at tuebor.primals.eco/analysis/the-desk-in-the-mountains/\n\n"
            "31 services. 2-minute heartbeat. 1,822 pages. 10,815 nodes. "
            "A 2GB VPS watching over $4.9M in public education funding.\n\n"
            "This is how a phone on Starlink sees inside the membrane."
        ),
    },
}

def save_manual_posts():
    POSTS_DIR.mkdir(exist_ok=True)
    for platform, data in MANUAL_POSTS.items():
        fname = f"{platform}.txt"
        content = ""
        if "title" in data:
            content += f"TITLE: {data['title']}\n\n"
        content += f"PRIMAL: {data['primal']}\n\n"
        content += data["text"]
        (POSTS_DIR / fname).write_text(content)
    return list(MANUAL_POSTS.keys())


# ═══════════════════════════════════════════════════════════
# STATUS + MAIN
# ═══════════════════════════════════════════════════════════

ALL_PLATFORMS = ["x", "reddit", "bluesky", "mastodon", "linkedin",
                 "threads", "hackernews", "instagram", "tumblr", "substack"]
API_PLATFORMS = ["x", "reddit", "bluesky", "mastodon"]
MANUAL_PLATFORMS = ["linkedin", "threads", "hackernews", "instagram", "tumblr", "substack"]

def status():
    proof = load_proof()
    posted_keys = set()
    for p in proof.get("posts", []):
        key = p["platform"]
        if p.get("sub"):
            key += f"/{p['sub']}"
        posted_keys.add(key)

    print("═══ rEEd it — Ed the GAIA teacher ═══")
    print()
    print("  PRIMAL MAP:")
    for plat, info in PRIMALS.items():
        marker = "✔" if plat in posted_keys or any(k.startswith(plat) for k in posted_keys) else "○"
        print(f"    {marker} {info['symbol']:6s} {plat:14s} → {info['primal']:16s} {info['guide']}")
    print()

    print("  API PLATFORMS:")
    for plat in API_PLATFORMS:
        if plat == "reddit":
            for sub in REDDIT_POSTS:
                key = f"reddit/{sub}"
                marker = "✔" if key in posted_keys else "○"
                match = [p for p in proof["posts"] if p.get("sub") == sub] if marker == "✔" else []
                if match:
                    print(f"    {marker} r/{sub}: {match[0].get('url','?')}")
                else:
                    print(f"    {marker} r/{sub}")
        else:
            marker = "✔" if plat in posted_keys else "○"
            if marker == "✔":
                match = [p for p in proof["posts"] if p["platform"] == plat]
                print(f"    {marker} {plat}: {match[0].get('url', match[0].get('uri','?'))}")
            else:
                print(f"    {marker} {plat}")

    print()
    print("  MANUAL PLATFORMS (text in posts/):")
    for plat in MANUAL_PLATFORMS:
        txt_exists = (POSTS_DIR / f"{plat}.txt").exists()
        print(f"    {'◉' if txt_exists else '○'} {plat}: {'saved' if txt_exists else 'not yet saved'}")

    print()
    total = len(proof.get("posts", []))
    print(f"  {total} posts fired | {len(ALL_PLATFORMS)} platforms total")
    print()

def main():
    parser = argparse.ArgumentParser(description="rEEd it — Ed the GAIA teacher broadcasts")
    parser.add_argument("--platform", choices=API_PLATFORMS + ["all", "status", "save-manual"], default="status")
    parser.add_argument("--sub", help="Reddit subreddit (e.g. Detroit, Teachers)")
    parser.add_argument("--all-subs", action="store_true")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.status or args.platform == "status":
        status()
        return

    if args.platform == "save-manual":
        saved = save_manual_posts()
        print(f"  ✔ saved {len(saved)} manual post texts to posts/")
        for s in saved:
            print(f"    → posts/{s}.txt ({MANUAL_POSTS[s]['primal']})")
        return

    creds = load_creds()
    proof = load_proof()

    if args.dry_run:
        print("═══ DRY RUN — rEEd it ═══\n")

    # X / Twitter
    if args.platform in ("x", "all"):
        if "x" not in creds:
            print("  ✘ x: no credentials")
            print("    need: api_key, api_secret, access_token, access_token_secret")
            print("    → developer.x.com/portal → create project + app")
        elif args.dry_run:
            print(f"  ◎ x: {len(X_THREAD)}-tweet thread")
            for i, t in enumerate(X_THREAD):
                print(f"    [{i+1}] {t[:70]}...")
        else:
            result = post_x(creds)
            record_proof(result, proof)

    # Reddit
    if args.platform in ("reddit", "all"):
        if "reddit" not in creds:
            print("  ✘ reddit: no credentials")
            print("    need: client_id, client_secret, username, password")
            print("    → reddit.com/prefs/apps → create 'script' app")
        else:
            subs = ([args.sub] if args.sub else
                    list(REDDIT_POSTS.keys()) if (args.all_subs or args.platform == "all") else [])
            if not subs:
                print("  ✘ reddit: specify --sub NAME or --all-subs")
            for sub in subs:
                if args.dry_run:
                    print(f"  ◎ r/{sub}: \"{REDDIT_POSTS[sub]['title'][:60]}...\"")
                else:
                    result = post_reddit(sub, creds)
                    record_proof(result, proof)

    # Bluesky
    if args.platform in ("bluesky", "all"):
        if "bluesky" not in creds:
            print("  ✘ bluesky: no credentials")
            print("    need: handle, password (app password)")
            print("    → bsky.app/settings/app-passwords")
        elif args.dry_run:
            print(f"  ◎ bluesky: \"{BLUESKY_POST[:60]}...\"")
        else:
            result = post_bluesky(creds)
            record_proof(result, proof)

    # Mastodon
    if args.platform in ("mastodon", "all"):
        if "mastodon" not in creds:
            print("  ✘ mastodon: no credentials")
            print("    need: access_token, instance_url")
            print("    → {instance}/settings/applications")
        elif args.dry_run:
            print(f"  ◎ mastodon: \"{MASTODON_POST[:60]}...\"")
        else:
            result = post_mastodon(creds)
            record_proof(result, proof)

    # Save manual posts
    if args.platform == "all":
        print()
        saved = save_manual_posts()
        print(f"  ✔ {len(saved)} manual posts saved to posts/")
        for s in saved:
            print(f"    → {s}.txt ({MANUAL_POSTS[s]['primal']})")

    if not args.dry_run and proof.get("posts"):
        push_proof_to_membrane(proof)

    print("\n═══ rEEd it — Ed teaches ═══")

if __name__ == "__main__":
    main()

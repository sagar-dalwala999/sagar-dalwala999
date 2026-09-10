"""Regenerate assets/stats.svg, langs.svg and activity.svg from live GitHub data.

Runs in the 'Refresh profile cards' workflow (GH_TOKEN provided) — or locally:
    GH_TOKEN=ghp_... python .github/scripts/gen_stats.py
    python .github/scripts/gen_stats.py --mock      # sample numbers, no network
"""
import os, sys, json, datetime, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import content as C
from style_theme import Theme
from svgkit import minify

QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    followers { totalCount }
    pullRequests { totalCount }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false, orderBy: {field: UPDATED_AT, direction: DESC}) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } }
      }
    }
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar { totalContributions weeks { contributionDays { contributionCount } } }
    }
  }
}"""

LANG_GROUPS = {"HTML": "HTML/CSS", "CSS": "HTML/CSS", "SCSS": "HTML/CSS", "Less": "HTML/CSS",
               "Jupyter Notebook": "Python"}


def fetch():
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit("GH_TOKEN (or GITHUB_TOKEN) is required — or pass --mock")
    to = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    frm = to - datetime.timedelta(days=365)
    body = json.dumps({"query": QUERY, "variables": {"login": C.STATS_USER, "from": frm.isoformat(), "to": to.isoformat()}}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", data=body,
                                 headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                                          "User-Agent": f"{C.HANDLE}-profile-cards"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    if "errors" in data:
        sys.exit(f"GraphQL errors: {data['errors']}")
    return data["data"]["user"]


def summarise(u):
    repos = u["repositories"]["nodes"]
    stats = {
        "repos": u["repositories"]["totalCount"],
        "followers": u["followers"]["totalCount"],
        "contributions": u["contributionsCollection"]["contributionCalendar"]["totalContributions"],
        "hackathons": len(C.WINS),
        "stars": sum(r["stargazerCount"] for r in repos),
        "prs": u["pullRequests"]["totalCount"],
    }
    sizes = {}
    for r in repos:
        for e in r["languages"]["edges"]:
            name = LANG_GROUPS.get(e["node"]["name"], e["node"]["name"])
            sizes[name] = sizes.get(name, 0) + e["size"]
    total = sum(sizes.values()) or 1
    top = sorted(sizes.items(), key=lambda kv: -kv[1])[:4]
    langs = [(n, round(100 * s / total)) for n, s in top]
    other = 100 - sum(p for _, p in langs)
    if other > 0:
        langs.append(("Other", other))
    weeks = u["contributionsCollection"]["contributionCalendar"]["weeks"][-52:]
    activity = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in weeks]
    return stats, langs, activity


def main():
    if "--mock" in sys.argv:
        from base import sample_activity
        stats, langs, activity = dict(C.STATS_SAMPLE), list(C.LANGS_SAMPLE), sample_activity()
    else:
        stats, langs, activity = summarise(fetch())
    S = Theme()
    os.makedirs(f"{ROOT}/assets", exist_ok=True)
    for name, svg in (("stats.svg", S.stats_card(stats)), ("langs.svg", S.langs_card(langs)), ("activity.svg", S.activity_card(activity))):
        open(f"{ROOT}/assets/{name}", "w").write(minify(svg))
    print("stats:", stats)
    print("langs:", langs)
    print("activity (weekly):", activity)


if __name__ == "__main__":
    main()

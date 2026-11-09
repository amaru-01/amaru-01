#!/usr/bin/env python3
"""Generate an all-time public GitHub contribution radar chart."""

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import urllib.error
import urllib.request

LOGIN = "amaru-01"
OUTPUT = Path("assets/contribution-activity.svg")
GRAPHQL_URL = "https://api.github.com/graphql"
QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to, includePrivateContributions: false) {
      totalCommitContributions
      totalIssueContributions
      totalPullRequestContributions
      totalPullRequestReviewContributions
    }
  }
}
"""
FIELDS = {
    "Commits": "totalCommitContributions",
    "Issues": "totalIssueContributions",
    "Pull requests": "totalPullRequestContributions",
    "Code reviews": "totalPullRequestReviewContributions",
}

def graphql(token: str, start: str, end: str) -> dict:
    body = json.dumps({
        "query": QUERY,
        "variables": {"login": LOGIN, "from": start, "to": end},
    }).encode()
    request = urllib.request.Request(
        GRAPHQL_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "profile-contribution-chart",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.load(response)
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub GraphQL request failed ({error.code}): {detail}") from error
    if result.get("errors"):
        raise RuntimeError(f"GitHub GraphQL returned errors: {result['errors']}")
    profile = result.get("data", {}).get("user")
    if profile is None:
        raise RuntimeError(f"GitHub user {LOGIN!r} was not found or is not accessible")
    return profile["contributionsCollection"]

def all_time_totals(token: str) -> dict:
    now = datetime.now(timezone.utc)
    totals = {label: 0 for label in FIELDS}
    for year in range(2008, now.year + 1):
        start = f"{year}-01-01T00:00:00Z"
        end = (
            f"{year + 1}-01-01T00:00:00Z"
            if year < now.year
            else now.isoformat().replace("+00:00", "Z")
        )
        collection = graphql(token, start, end)
        for label, field in FIELDS.items():
            totals[label] += collection[field]
    return totals

def make_svg(totals: dict) -> str:
    labels = ["Code reviews", "Issues", "Pull requests", "Commits"]
    values = [totals[label] for label in labels]
    total = sum(values)
    percentages = [value * 100 / total if total else 0 for value in values]

    cx, cy, radius = 500, 300, 180
    endpoints = [(cx, cy - radius), (cx + radius, cy), (cx, cy + radius), (cx - radius, cy)]
    points = []
    for (x, y), percentage in zip(endpoints, percentages):
        scale = percentage / 100
        points.append((cx + (x - cx) * scale, cy + (y - cy) * scale))
    polygon_points = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)

    axes = "\n".join(
        f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" class="axis" />'
        for x, y in endpoints
    )
    markers = "\n".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" class="marker" />'
        for x, y in points
    )
    value_labels = [
        f'<text x="{cx}" y="{cy - radius * p / 100 - 13:.1f}" text-anchor="middle" class="value">{p:.1f}%</text>',
        f'<text x="{cx + radius * p / 100 + 12:.1f}" y="{cy + 5}" class="value">{p:.1f}%</text>',
        f'<text x="{cx}" y="{cy + radius * p / 100 + 23:.1f}" text-anchor="middle" class="value">{p:.1f}%</text>',
        f'<text x="{cx - radius * p / 100 - 12:.1f}" y="{cy + 5}" text-anchor="end" class="value">{p:.1f}%</text>',
    ]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="600" viewBox="0 0 1000 600" role="img" aria-labelledby="title desc">
  <title id="title">All-time public GitHub contributions for {LOGIN}</title>
  <desc id="desc">{total:,} public contributions: {totals['Code reviews']:,} code reviews, {totals['Issues']:,} issues, {totals['Pull requests']:,} pull requests, and {totals['Commits']:,} commits.</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1020"/><stop offset="1" stop-color="#17142e"/></linearGradient>
    <linearGradient id="area" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#22c55e" stop-opacity=".55"/><stop offset="1" stop-color="#06b6d4" stop-opacity=".3"/></linearGradient>
  </defs>
  <style>.axis{{stroke:#22c55e;stroke-width:2}} .marker{{fill:#f8fafc;stroke:#22c55e;stroke-width:2}} .value{{fill:#67e8f9;font:13px Inter,Segoe UI,Arial,sans-serif}}</style>
  <rect width="1000" height="600" rx="28" fill="url(#bg)"/>
  <text x="52" y="58" fill="#f8fafc" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="25" font-weight="700">All-time contribution activity</text>
  <text x="52" y="86" fill="#94a3b8" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="14">Public contributions only · {total:,} total</text>
  <g stroke="#334155" fill="none"><polygon points="500,120 680,300 500,480 320,300"/><polygon points="500,165 635,300 500,435 365,300"/><polygon points="500,210 590,300 500,390 410,300"/><polygon points="500,255 545,300 500,345 455,300"/></g>
  <g>{axes}</g>
  <polygon points="{polygon_points}" fill="url(#area)" stroke="#22c55e" stroke-width="3" stroke-linejoin="round"/>
  <g>{markers}</g>
  <g font-family="Inter,Segoe UI,Arial,sans-serif" font-size="15" fill="#cbd5e1">
    <text x="500" y="112" text-anchor="middle">Code reviews · {totals['Code reviews']:,}</text>
    <text x="700" y="305">Issues · {totals['Issues']:,}</text>
    <text x="500" y="515" text-anchor="middle">Pull requests · {totals['Pull requests']:,}</text>
    <text x="300" y="305" text-anchor="end">Commits · {totals['Commits']:,}</text>
  </g>
  <g>{''.join(value_labels)}</g>
  <text x="52" y="565" fill="#64748b" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="12">Generated from GitHub contribution data; private activity is excluded.</text>
</svg>
'''

def main() -> None:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN environment variable is required")
    totals = all_time_totals(token)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(make_svg(totals), encoding="utf-8")
    print(f"Updated {OUTPUT}: {sum(totals.values()):,} public contributions")

if __name__ == "__main__":
    main()
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
    contributionsCollection(from: $from, to: $to) {
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
    # Axis order: top, right, bottom, left (matches GitHub's activity overview).
    labels = ["Code review", "Issues", "Pull requests", "Commits"]
    keys = ["Code reviews", "Issues", "Pull requests", "Commits"]
    values = [totals[key] for key in keys]
    total = sum(values)
    percentages = [value * 100 / total if total else 0 for value in values]

    width, height = 420, 340
    cx, cy, radius = 210, 165, 100
    endpoints = [(cx, cy - radius), (cx + radius, cy), (cx, cy + radius), (cx - radius, cy)]
    points = [
        (cx + (x - cx) * p / 100, cy + (y - cy) * p / 100)
        for (x, y), p in zip(endpoints, percentages)
    ]
    polygon_points = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)

    axes = "".join(
        f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" class="axis" />'
        for x, y in endpoints
    )
    markers = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" class="marker" />'
        for x, y in points
    )

    def label(x, y_pct, y_name, anchor, i):
        return (
            f'<text x="{x}" y="{y_pct}" text-anchor="{anchor}">{percentages[i]:.0f}%</text>'
            f'<text x="{x}" y="{y_name}" text-anchor="{anchor}">{labels[i]}</text>'
        )

    text = "".join([
        label(cx, cy - radius - 36, cy - radius - 18, "middle", 0),
        label(cx + radius + 14, cy - 2, cy + 16, "start", 1),
        label(cx, cy + radius + 28, cy + radius + 46, "middle", 2),
        label(cx - radius - 14, cy - 2, cy + 16, "end", 3),
    ])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">All-time public GitHub contributions for {LOGIN}</title>
  <desc id="desc">{total:,} public contributions: {totals['Code reviews']:,} code reviews, {totals['Issues']:,} issues, {totals['Pull requests']:,} pull requests, and {totals['Commits']:,} commits.</desc>
  <style>
    .axis{{stroke:#4ade80;stroke-width:2}}
    .marker{{fill:#bbf7d0;stroke:#4ade80;stroke-width:2}}
    .area{{fill:#2ea04366;stroke:#4ade80;stroke-width:1.5;stroke-linejoin:round}}
    text{{fill:#c9d1d9;font:14px -apple-system,Segoe UI,Helvetica,Arial,sans-serif}}
    .note{{fill:#6e7681;font-size:11px}}
  </style>
  <rect width="{width}" height="{height}" fill="#0d1117"/>
  <g>
    {axes}
  </g>
  <polygon points="{polygon_points}" class="area"/>
  <g>
    {markers}
  </g>
  <g>
    {text}
  </g>
  <text x="{width // 2}" y="{height - 10}" text-anchor="middle" class="note">{total:,} public contributions · all time</text>
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
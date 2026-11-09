#!/usr/bin/env python3
"""Generate an all-time public GitHub activity dashboard (single SVG grid).

Panels: contribution-mix radar, contributions per year, and stat tiles
(total, longest streak, current streak, most active year).
"""

from datetime import date, datetime, timezone
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
      contributionCalendar {
        weeks {
          contributionDays {
            date
            contributionCount
          }
        }
      }
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
FONT = "-apple-system,Segoe UI,Helvetica,Arial,sans-serif"


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


def collect(token: str) -> dict:
    """Fetch per-year totals, all-time totals and daily counts."""
    now = datetime.now(timezone.utc)
    totals = {label: 0 for label in FIELDS}
    yearly: dict[int, int] = {}
    days: dict[str, int] = {}
    for year in range(2008, now.year + 1):
        start = f"{year}-01-01T00:00:00Z"
        end = (
            f"{year + 1}-01-01T00:00:00Z"
            if year < now.year
            else now.isoformat().replace("+00:00", "Z")
        )
        collection = graphql(token, start, end)
        year_total = 0
        for label, field in FIELDS.items():
            totals[label] += collection[field]
            year_total += collection[field]
        yearly[year] = year_total
        for week in collection["contributionCalendar"]["weeks"]:
            for day in week["contributionDays"]:
                days[day["date"]] = day["contributionCount"]
    return {"totals": totals, "yearly": yearly, "days": days}


def streaks(days: dict[str, int]) -> tuple[int, int]:
    """Return (longest, current) streaks of consecutive days with activity."""
    today = date.today()
    longest = run = 0
    previous = None
    for key in sorted(days):
        day = date.fromisoformat(key)
        if day > today:
            continue
        if days[key] > 0:
            run = run + 1 if previous and (day - previous).days == 1 else 1
            longest = max(longest, run)
            previous = day
        else:
            run = 0
            previous = None
    # Current streak: walk back from today; today may still be empty.
    current = 0
    cursor = today
    if days.get(cursor.isoformat(), 0) == 0:
        cursor = date.fromordinal(cursor.toordinal() - 1)
    while days.get(cursor.isoformat(), 0) > 0:
        current += 1
        cursor = date.fromordinal(cursor.toordinal() - 1)
    return longest, current


def radar(totals: dict, x0: int, y0: int) -> str:
    labels = ["Code review", "Issues", "Pull requests", "Commits"]
    keys = ["Code reviews", "Issues", "Pull requests", "Commits"]
    total = sum(totals.values())
    pct = [totals[k] * 100 / total if total else 0 for k in keys]
    cx, cy, r = x0 + 140, y0 + 170, 76
    ends = [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]
    pts = [(cx + (x - cx) * p / 100, cy + (y - cy) * p / 100) for (x, y), p in zip(ends, pct)]
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    axes = "".join(f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" class="axis"/>' for x, y in ends)
    marks = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" class="marker"/>' for x, y in pts)

    def lab(i, x, y1, y2, anchor):
        return (
            f'<text x="{x}" y="{y1}" text-anchor="{anchor}" class="val">{pct[i]:.0f}%</text>'
            f'<text x="{x}" y="{y2}" text-anchor="{anchor}" class="sub">{labels[i]}</text>'
        )

    text = "".join([
        lab(0, cx, cy - r - 34, cy - r - 17, "middle"),
        lab(1, cx + r + 12, cy - 3, cy + 14, "start"),
        lab(2, cx, cy + r + 26, cy + r + 43, "middle"),
        lab(3, cx - r - 12, cy - 3, cy + 14, "end"),
    ])
    return (
        f'<text x="{x0 + 20}" y="{y0 + 30}" class="title">Contribution mix</text>'
        f'{axes}<polygon points="{poly}" class="area"/>{marks}{text}'
    )


def bars(yearly: dict[int, int], x0: int, y0: int, w: int, h: int) -> str:
    first = next((y for y in sorted(yearly) if yearly[y] > 0), None)
    out = [f'<text x="{x0 + 20}" y="{y0 + 30}" class="title">Contributions per year</text>']
    if first is None:
        return out[0]
    years = [y for y in sorted(yearly) if y >= first]
    peak = max(yearly[y] for y in years) or 1
    base = y0 + h - 28
    top = y0 + 62
    slot = (w - 40) / len(years)
    bar_w = min(44, slot * 0.6)
    for i, year in enumerate(years):
        value = yearly[year]
        bh = max(2, (base - top) * value / peak) if value else 0
        cx = x0 + 20 + slot * (i + 0.5)
        if value:
            out.append(f'<rect x="{cx - bar_w / 2:.1f}" y="{base - bh:.1f}" width="{bar_w:.1f}" height="{bh:.1f}" rx="3" class="bar"/>')
        out.append(f'<text x="{cx:.1f}" y="{base - bh - 6:.1f}" text-anchor="middle" class="sub">{value:,}</text>')
        out.append(f'<text x="{cx:.1f}" y="{base + 18}" text-anchor="middle" class="sub">{year}</text>')
    out.append(f'<line x1="{x0 + 20}" y1="{base}" x2="{x0 + w - 20}" y2="{base}" class="grid"/>')
    return "".join(out)


def tiles(items: list[tuple[str, str]], x0: int, y0: int, w: int, h: int) -> str:
    gap = 12
    tw = (w - gap * (len(items) - 1)) / len(items)
    out = []
    for i, (value, label) in enumerate(items):
        x = x0 + i * (tw + gap)
        out.append(
            f'<rect x="{x:.1f}" y="{y0}" width="{tw:.1f}" height="{h}" rx="8" class="card"/>'
            f'<text x="{x + tw / 2:.1f}" y="{y0 + h / 2 + 2:.1f}" text-anchor="middle" class="big">{value}</text>'
            f'<text x="{x + tw / 2:.1f}" y="{y0 + h / 2 + 24:.1f}" text-anchor="middle" class="sub">{label}</text>'
        )
    return "".join(out)


def make_svg(data: dict) -> str:
    totals, yearly, days = data["totals"], data["yearly"], data["days"]
    total = sum(totals.values())
    longest, current = streaks(days)
    best_year = max(yearly, key=yearly.get) if any(yearly.values()) else None

    W, H = 900, 360
    items = [
        (f"{total:,}", "Public contributions"),
        (f"{longest} day{'s' if longest != 1 else ''}", "Longest streak"),
        (f"{current} day{'s' if current != 1 else ''}", "Current streak"),
        (str(best_year) if best_year else "–", "Most active year"),
    ]
    px = 316  # right column start
    pw = W - px - 16
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
  <title id="title">All-time public GitHub activity for {LOGIN}</title>
  <desc id="desc">{total:,} public contributions: {totals['Code reviews']:,} code reviews, {totals['Issues']:,} issues, {totals['Pull requests']:,} pull requests and {totals['Commits']:,} commits. Longest streak {longest} days, current streak {current} days.</desc>
  <style>
    text{{fill:#c9d1d9;font-family:{FONT}}}
    .title{{font-size:14px;font-weight:600;fill:#f0f6fc}}
    .val{{font-size:14px}}
    .sub{{font-size:12px;fill:#8b949e}}
    .big{{font-size:22px;font-weight:700;fill:#f0f6fc}}
    .axis{{stroke:#4ade80;stroke-width:2}}
    .marker{{fill:#bbf7d0;stroke:#4ade80;stroke-width:2}}
    .area{{fill:#2ea04366;stroke:#4ade80;stroke-width:1.5;stroke-linejoin:round}}
    .bar{{fill:#2ea043}}
    .grid{{stroke:#30363d;stroke-width:1}}
    .card{{fill:#161b22;stroke:#30363d}}
  </style>
  <rect width="{W}" height="{H}" rx="12" fill="#0d1117" stroke="#30363d"/>
  <rect x="16" y="16" width="284" height="{H - 32}" rx="8" class="card"/>
  <rect x="{px}" y="16" width="{pw}" height="214" rx="8" class="card"/>
  {radar(totals, 16, 16)}
  {bars(yearly, px, 16, pw, 214)}
  {tiles(items, px, 246, pw, 98)}
</svg>
'''


def main() -> None:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN environment variable is required")
    data = collect(token)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(make_svg(data), encoding="utf-8")
    print(f"Updated {OUTPUT}: {sum(data['totals'].values()):,} public contributions")


if __name__ == "__main__":
    main()

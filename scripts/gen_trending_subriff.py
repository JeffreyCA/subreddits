"""
Retrieves trending subreddits from subriff.com and produces a blended list.

Algorithm:
1. Query multiple size filters for both daily and weekly
2. Count appearances across all queries (more appearances = more reliably trending)
3. Sort by appearance count, take top N
"""

import sys
import requests
from collections import Counter

BASE_URL = "https://subriff.com/Home/GetSubreddits"
SIZE_FILTERS = ["medium-small", "medium", "large", "xlarge"]
SORT_PERIODS = ["daily", "weekly"]
FINAL_OUTPUT_LIMIT = 35


def fetch_subreddits(size_filter: str, sort_by: str) -> list[str]:
    """Fetch subreddit names from subriff.com API."""
    params = {
        "page": 1,
        "sizeFilter": size_filter,
        "searchTerm": "",
        "sortBy": sort_by,
        "growthType": "percent",
        "sortColumn": "",
        "sortDirection": "",
        "dateFilter": "all",
        "allowsPromotion": "false",
        "nsfw": "false",
    }
    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    
    names = []
    for sub in data.get("subreddits", []):
        # Skip if any NSFW flag is true
        if (
            sub.get("isNsfw")
            or sub.get("internal_IsNsfw")
            or sub.get("suggested_Internal_IsNsfw")
        ):
            continue
        name = sub.get("displayName", "")
        if name:
            names.append(name)
    return names


def generate_blended_trending() -> list[str]:
    """Generate a blended list of trending subreddits.

    Raises:
        RuntimeError: if any query fails. A partial result would skew the
            blended ranking, so we abort entirely rather than emit degraded
            output (which the caller would otherwise commit).
    """
    appearances = Counter()
    failures = []

    for size_filter in SIZE_FILTERS:
        for sort_by in SORT_PERIODS:
            try:
                names = fetch_subreddits(size_filter, sort_by)
                appearances.update(names)
            except Exception as e:
                # Warnings go to stderr so they never pollute stdout, which is
                # redirected into the output file.
                print(
                    f"Warning: Failed to fetch {size_filter}/{sort_by}: {e}",
                    file=sys.stderr,
                )
                failures.append(f"{size_filter}/{sort_by}")

    if failures:
        raise RuntimeError(
            f"Aborting: {len(failures)} fetch(es) failed: {', '.join(failures)}"
        )

    # Sort by appearance count (descending), take top N
    top = appearances.most_common(FINAL_OUTPUT_LIMIT)
    return [name for name, _ in top]


if __name__ == "__main__":
    try:
        subreddits = generate_blended_trending()
    except RuntimeError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    if not subreddits:
        print("Aborting: no subreddits found", file=sys.stderr)
        sys.exit(1)

    for subreddit in subreddits:
        print(subreddit)

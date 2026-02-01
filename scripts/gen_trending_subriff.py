"""
Retrieves trending subreddits from subriff.com and produces a blended list.

Algorithm:
1. Query multiple size filters (medium-small, medium, large, xlarge) for both daily and weekly
2. Assign a composite score based on:
   - Growth percentage (normalized within each query)
   - Position in results (earlier = higher score)
   - Bonus for appearing in multiple queries (both daily and weekly trending)
3. Diversify by taking top N from each size category, then merge and deduplicate
4. Output a well-rounded list sorted by composite score
"""

import requests
from collections import defaultdict
from dataclasses import dataclass, field

BASE_URL = "https://subriff.com/Home/GetSubreddits"
SIZE_FILTERS = ["medium-small", "medium", "large", "xlarge"]
SORT_PERIODS = ["daily", "weekly"]
RESULTS_PER_QUERY = 20  # API returns 20 per page
TOP_PER_SIZE_CATEGORY = 5  # Take top N from each size filter
FINAL_OUTPUT_LIMIT = 30  # Final blended list size


@dataclass
class SubredditScore:
    """Tracks scoring data for a subreddit across multiple queries."""
    name: str
    subscribers: int = 0
    daily_growth_pct: float = 0.0
    weekly_growth_pct: float = 0.0
    daily_rank: int | None = None  # Position in daily results (0-indexed)
    weekly_rank: int | None = None  # Position in weekly results (0-indexed)
    size_filter: str = ""
    appearances: int = 0
    composite_score: float = 0.0


def fetch_subreddits(size_filter: str, sort_by: str) -> list[dict]:
    """Fetch subreddits from subriff.com API."""
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
    return data.get("subreddits", [])


def calculate_composite_score(sub: SubredditScore) -> float:
    """
    Calculate a composite score for ranking.
    
    Factors:
    - Position score: Higher score for appearing earlier in results
    - Multi-appearance bonus: Appears in both daily and weekly = more reliable trend
    - Growth strength: Normalized growth percentage contribution
    """
    score = 0.0
    
    # Position score (max 20 points per appearance, decaying by rank)
    if sub.daily_rank is not None:
        score += max(0, RESULTS_PER_QUERY - sub.daily_rank)
    if sub.weekly_rank is not None:
        score += max(0, RESULTS_PER_QUERY - sub.weekly_rank)
    
    # Multi-appearance bonus (appears in both daily and weekly trending)
    if sub.appearances >= 2:
        score += 15 * (sub.appearances - 1)
    
    # Growth contribution (normalized, max ~10 points each)
    # Cap extreme outliers
    daily_contrib = min(sub.daily_growth_pct, 100) / 10
    weekly_contrib = min(sub.weekly_growth_pct, 500) / 50
    score += daily_contrib + weekly_contrib
    
    return score


def generate_blended_trending() -> list[str]:
    """Generate a blended list of trending subreddits."""
    # Track all subreddits by name
    subreddit_data: dict[str, SubredditScore] = {}
    
    # Track subreddits by size category for diversity
    by_size_category: dict[str, list[str]] = defaultdict(list)
    
    for size_filter in SIZE_FILTERS:
        for sort_by in SORT_PERIODS:
            try:
                results = fetch_subreddits(size_filter, sort_by)
            except Exception as e:
                print(f"Warning: Failed to fetch {size_filter}/{sort_by}: {e}")
                continue
            
            for rank, sub in enumerate(results):
                name = sub.get("displayName", "")
                if not name:
                    continue
                
                # Skip if any NSFW flag is true
                if (
                    sub.get("isNsfw")
                    or sub.get("internal_IsNsfw")
                    or sub.get("suggested_Internal_IsNsfw")
                ):
                    continue
                
                # Initialize or update subreddit data
                if name not in subreddit_data:
                    subreddit_data[name] = SubredditScore(
                        name=name,
                        subscribers=sub.get("subscribers", 0),
                        daily_growth_pct=sub.get("dailyGrowthPercentage", 0) or 0,
                        weekly_growth_pct=sub.get("weeklyGrowthPercentage", 0) or 0,
                        size_filter=size_filter,
                    )
                    by_size_category[size_filter].append(name)
                
                entry = subreddit_data[name]
                entry.appearances += 1
                
                # Update rank based on sort period
                if sort_by == "daily":
                    if entry.daily_rank is None or rank < entry.daily_rank:
                        entry.daily_rank = rank
                else:  # weekly
                    if entry.weekly_rank is None or rank < entry.weekly_rank:
                        entry.weekly_rank = rank
                
                # Update growth percentages (take max seen)
                entry.daily_growth_pct = max(
                    entry.daily_growth_pct,
                    sub.get("dailyGrowthPercentage", 0) or 0
                )
                entry.weekly_growth_pct = max(
                    entry.weekly_growth_pct,
                    sub.get("weeklyGrowthPercentage", 0) or 0
                )
    
    # Calculate composite scores
    for entry in subreddit_data.values():
        entry.composite_score = calculate_composite_score(entry)
    
    # Strategy: Take top performers from each size category to ensure diversity
    # Then fill remaining slots with highest overall scores
    selected: set[str] = set()
    final_list: list[tuple[str, float]] = []
    
    # Phase 1: Take top N from each size category
    for size_filter in SIZE_FILTERS:
        category_subs = by_size_category[size_filter]
        # Sort by composite score within category
        sorted_category = sorted(
            category_subs,
            key=lambda n: subreddit_data[n].composite_score,
            reverse=True
        )
        for name in sorted_category[:TOP_PER_SIZE_CATEGORY]:
            if name not in selected:
                selected.add(name)
                final_list.append((name, subreddit_data[name].composite_score))
    
    # Phase 2: Fill remaining slots with highest overall scores (not yet selected)
    remaining_slots = FINAL_OUTPUT_LIMIT - len(final_list)
    if remaining_slots > 0:
        all_sorted = sorted(
            subreddit_data.values(),
            key=lambda s: s.composite_score,
            reverse=True
        )
        for entry in all_sorted:
            if entry.name not in selected:
                selected.add(entry.name)
                final_list.append((entry.name, entry.composite_score))
                if len(final_list) >= FINAL_OUTPUT_LIMIT:
                    break
    
    # Sort final list by composite score
    final_list.sort(key=lambda x: x[1], reverse=True)
    
    return [name for name, _ in final_list]


if __name__ == "__main__":
    trending = generate_blended_trending()
    for subreddit in trending:
        print(subreddit)

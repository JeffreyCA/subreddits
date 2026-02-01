# Subreddits

## [popular.txt](https://jeffreyca.github.io/subreddits/popular.txt)
List of popular subreddits retrieved using [Reddit's popular subreddits API](https://www.reddit.com/dev/api/#GET_subreddits_{where}). Updated weekly.

To generate the list yourself, you'll need a Reddit app client ID and secret, which you can get from https://reddit.com/prefs/apps.

### Generate using GitHub Actions
1. Set the following repository secrets ([guide](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions#creating-secrets-for-a-repository)) to the values from previous step:
    - `REDDIT_CLIENT_ID`
    - `REDDIT_CLIENT_SECRET`
2. The GitHub Action "Update popular subreddits" is configured to run at 00:00 UTC on Sundays and Wednesdays, but you can also manually trigger it.

### Generate from local machine
1. Install Python 3
2. `pip install -r requirements.txt`
3. Set the `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET` environment variables
4. `python scripts/gen_popular.py`

## [trending-subriff-blended.txt](https://jeffreyca.github.io/subreddits/trending-subriff-blended.txt)
List of trending subreddits, sourced from [subriff.com](https://subriff.com/). Updated daily.

* Growth period: daily, weekly (blended)
* Size: medium-small, medium, large, xlarge

### Generate using GitHub Actions
The GitHub Action "Update trending subreddits (subriff)" is configured to run twice a day, but you can also manually trigger it.

### Generate from local machine
1. Install Python 3
2. `pip install -r requirements.txt`
3. `python scripts/gen_trending_subriff.py`

## [trending-gummy-daily.txt](https://jeffreyca.github.io/subreddits/trending-gummy-daily.txt), [trending-gummy-weekly.txt](https://jeffreyca.github.io/subreddits/trending-gummy-weekly.txt)
List of trending subreddits, sourced from [gummysearch.com](https://gummysearch.com/tools/top-subreddits/). **No longer updated.**

* Growth period: daily, weekly
* Size: large, huge, massive

### Generate using GitHub Actions
The GitHub Action "Update trending subreddits (gummysearch)" is configured to run twice a day, but you can also manually trigger it.

### Generate from local machine
1. `./scripts/gen_trending_gummy.sh <daily or weekly>`

## [trending-reddstats-daily.txt](https://jeffreyca.github.io/subreddits/trending-reddstats-daily.txt), [trending-reddstats-weekly.txt](https://jeffreyca.github.io/subreddits/trending-reddstats-weekly.txt)
List of trending subreddits, sourced from [reddstats.com](https://reddstats.com/ranking/relative?over18=False&period=daily&subscriber_classification=50001-100000). **No longer updated.**

## [trending-apollo.txt](https://jeffreyca.github.io/subreddits/trending-apollo.txt)
Original list of trending subreddits used by Apollo iOS app, extracted from `trending-subreddits.plist`. Last updated 2023-09-09.

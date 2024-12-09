# Subreddit Lists

## popular.txt ([link](https://jeffreyca.github.io/subreddit-lists/popular.txt))
List of popular subreddits retrieved using [Reddit's popular subreddits API](https://www.reddit.com/dev/api/#GET_subreddits_{where}). Updated daily.

To generate the list yourself, you'll need a Reddit app client ID and secret, which you can get by following these steps:

1. Sign into your Reddit account and go to https://reddit.com/prefs/apps
2. Click the `are you a developer? create an app...` button
3. Fill in the fields
    - Name: *anything*
    - Choose `Script`
    - Description: *anything*
    - About url: *anything*
    - Redirect uri: *anything* (e.g. `https://example.com`)

4. Click `create app`
5. After creating the app you'll get a **client ID** as well as a **secret**, which will both be a random string of characters.

### Generate using GitHub Actions
1. Set the following repository secrets ([guide](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions#creating-secrets-for-a-repository)) to the values from previous step:
    - `REDDIT_CLIENT_ID`
    - `REDDIT_CLIENT_SECRET`
2. The GitHub Action "Update popular subreddits" is configured to run at 00:00 UTC daily, but you can also manually trigger it.

### Generate from local machine
1. Install Python 3
2. `pip install -r requirements.txt`
3. Set the `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET` environment variables
4. `python gen_popular.py`

## trending-original.txt ([link](https://jeffreyca.github.io/subreddit-lists/trending-original.txt))
Original list of trending subreddits used by Apollo iOS app, extracted from `trending-subreddits.plist`. Last updated 2023-09-09.
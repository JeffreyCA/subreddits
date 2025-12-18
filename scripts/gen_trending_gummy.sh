#!/bin/bash

if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
    echo "Usage: $0 <daily|weekly> [curl_wrapper]"
    exit 1
fi

period=$1
if [ "$period" != "daily" ] && [ "$period" != "weekly" ]; then
    echo "Invalid period. Must be 'daily' or 'weekly'."
    exit 1
fi

# Curl wrapper command (e.g., curl_chrome99, curl_chrome142), defaults to curl_chrome142
CURL_CMD="${2:-curl_chrome142}"

urls=(
  "https://gummysearch.com/page-data/tools/top-subreddits/size-large/page-data.json"
  "https://gummysearch.com/page-data/tools/top-subreddits/size-huge/page-data.json"
  "https://gummysearch.com/page-data/tools/top-subreddits/size-massive/page-data.json"
)

LIMIT_PER_BIN=7

for url in "${urls[@]}"; do
    if ! $CURL_CMD -s "$url" | jq -r ".result.pageContext.lists.growth_${period}[].name" | head -n $LIMIT_PER_BIN; then
        echo "Failed to download or process $url"
        exit 1
    fi
done

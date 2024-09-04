#!/bin/bash

# Usage: ./test.sh <url> <number_of_requests> <concurrency>

URL=$1
NUM_REQUESTS=$2
CONCURRENCY=$3

if [[ -z "$URL" || -z "$NUM_REQUESTS" || -z "$CONCURRENCY" ]]; then
  echo "Usage: ./test.sh <url> <number_of_requests> <concurrency>"
  exit 1
fi

# Function to send a single curl request
send_request() {
  global URL
  echo "$URL"
  local result=$(curl -s -o /dev/null -w "%{http_code}" "$url")
  echo "Response code: $result"
}

# Export the function to be used by xargs
export -f send_request

# Generate the required number of request jobs
for i in $(seq 1 $NUM_REQUESTS); do echo $i; done | xargs -n 1 -P $CONCURRENCY -I {} bash -c "curl $URL"

echo "\nFinished sending $NUM_REQUESTS requests to $URL with concurrency $CONCURRENCY"

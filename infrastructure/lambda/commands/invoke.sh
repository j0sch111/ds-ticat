#!/bin/bash

# Set the URL of your Docker container
CONTAINER_URL="http://localhost:8080/2015-03-31/functions/function/invocations"

# Set the input text for sentiment analysis
INPUT_TEXT="This product is fantastic!"

# Create the JSON payload
PAYLOAD=$(cat <<EOF
{
  "body": "{\"text\": \"$INPUT_TEXT\"}"
}
EOF
)

# Send the request to the Docker container
curl -X POST $CONTAINER_URL \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" \
  | python -m json.tool  # This pipes the output to Python's json.tool for pretty-printing

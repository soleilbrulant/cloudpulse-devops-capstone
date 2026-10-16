#!/usr/bin/env bash
# Generates continuous load against the CloudPulse backend API to demonstrate HPA autoscaling
TARGET_URL=${1:-"http://localhost:8000/api/assets"}
CONCURRENCY=${2:-10}

echo "Generating synthetic HTTP traffic on ${TARGET_URL} with concurrency ${CONCURRENCY}..."
echo "Watch autoscaling with: kubectl get hpa -n cloudpulse -w"

while true; do
  for i in $(seq 1 $CONCURRENCY); do
    curl -s "${TARGET_URL}" > /dev/null &
  done
  wait
  sleep 0.1
done

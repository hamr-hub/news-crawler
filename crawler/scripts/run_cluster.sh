#!/bin/bash

echo "Starting News Crawler Cluster..."

# Start Redis
docker run -d --name news-redis -p 6379:6379 redis:alpine

# Wait for Redis to be ready
sleep 3

# Start 3 Crawler Worker nodes
for i in {1..3}
do
   echo "Starting Worker $i..."
   # In a real environment, you'd build a docker image first
   # docker run -d --name news-worker-$i --network host news-crawler-image
done

echo "Cluster started. Spiders will pull tasks from Redis queue."

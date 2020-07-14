#!/usr/bin/env bash

echo "Waiting for Elasticsearch to launch on port 9200..."

while ! nc -z localhost 9200; do
  echo waiting for elasticsearch;
  sleep 2;
done

echo "Giving Elasticsearch some time to get ready"

# This needs to be changed to a CURL with wait_for_green but wan't working for some reason.
sleep 60
echo "Elasticsearch should be up"
#!/bin/sh
set -e
# start-cron.sh

while [ true ]; do
    github-release-notifier
    sleep 24h
done

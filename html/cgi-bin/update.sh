#!/bin/sh

# output HTTP header
echo "Content-Type: text/plain"
echo ""

# switch to repo directory
cd /var/www/html

# discard all changes to avoid "you have unstaged changes" error
git reset --hard

# store old revision hash
$OLD=$(git rev-parse HEAD)

# fetch new version from server
git pull --no-rebase

# show all commit messages since stored revision hash
git --no-pager log --pretty=format:'* %s' $OLD..
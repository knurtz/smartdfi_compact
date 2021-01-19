#!/bin/sh

# output HTTP header
echo "Content-Type: text/plain; charset=utf-8"
echo ""

# switch to repo directory
#cd /var/www/html

# discard all changes to avoid "you have unstaged changes" error
git reset --hard > /dev/null

# store old revision hash
OLD_HASH=$(git rev-parse HEAD)

# fetch new version from server
git pull --no-rebase > /dev/null

# get new hash to compare to old one
NEW_HASH=$(git rev-parse HEAD)

# show all commit messages since stored revision hash
echo "Änderungen seit letztem Update:"
git --no-pager log --pretty=format:'* %s' $OLD_HASH..
if [[ "$OLD_HASH" == "$NEW_HASH" ]]
then
	echo "Keine Änderungen gefunden."
fi
	
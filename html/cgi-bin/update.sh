#!/bin/sh

# output HTTP header
echo "Content-Type: text/plain; charset=utf-8"
echo ""
echo "Aktualisiere..."

# switch to repo directory
cd /var/www

# log update to file
echo "" >> ./html/cgi-bin/update-log.txt
echo "Updating repo on $(date)" >> ./html/cgi-bin/update-log.txt

# discard all changes to avoid "you have unstaged changes" error
git reset --hard > /dev/null 2>&1

# store old revision hash
OLD_HASH=$(git rev-parse HEAD)

# fetch new version from server, log to file
git pull --no-rebase >> ./html/cgi-bin/update-log.txt 2>&1

# show all commit messages since stored revision hash
if [[ "$OLD_HASH" == "$(git rev-parse HEAD)" ]]
then
	echo "Keine Änderungen gefunden."
else
	echo "Änderungen seit letztem Update:"
	git --no-pager log --pretty=format:'* %s' $OLD_HASH..
fi
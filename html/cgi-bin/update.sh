#!/bin/bash

# output HTTP header
echo "Content-Type: text/plain; charset=utf-8"
echo ""

# extract get parameters into an array with param[0] = key1, param[1] = value 1, param[2] = key2 etc.
saveIFS=$IFS
IFS='=&'
param=($QUERY_STRING)
IFS=$saveIFS

# check if version has been provided
VERSION="HEAD"
if [[ "${param[0]}" == "version" ]]; then
	VERSION=${param[1]}
	echo "Aktualisiere auf Version $VERSION"
else
	echo "Aktualisiere auf neuste Version."
fi

# switch to repo directory
cd /var/www

# log update to file
echo "" >> ./html/cgi-bin/update-log.txt
echo "======================" >> ./html/cgi-bin/update-log.txt
echo "Updating repo on $(date) to revision $VERSION" >> ./html/cgi-bin/update-log.txt

OLD_HASH=$(git rev-parse --short HEAD)
echo "Old hash: $OLD_HASH" >> ./html/cgi-bin/update-log.txt 2>&1

# fetch new versions from server
git fetch >> ./html/cgi-bin/update-log.txt 2>&1

# go to requested version
# if no specific revision is requested, this also cleans the working area for the upcoming pull command
git reset --soft $VERSION >> ./html/cgi-bin/update-log.txt 2>&1

# if no specific revision is requested, just forward to newest revision with git pull
if [[ "$VERSION" == "HEAD" ]]
then
	git pull --no-rebase >> ./html/cgi-bin/update-log.txt 2>&1
fi

NEW_HASH=$(git rev-parse --short HEAD)
echo "New hash: $NEW_HASH" >> ./html/cgi-bin/update-log.txt 2>&1

# display results
# check first possibility: no updates on server, same version as before
if [[ "$OLD_HASH" == "$NEW_HASH" ]]
then
	echo "Keine Änderungen gefunden."

# second possibility: went back to older version
elif [ $(git rev-list $OLD_HASH.. | wc -l) -eq 0 ]
then
	echo "Softwarestand jetzt auf Version [$(git rev-parse --short HEAD)]."
	echo "Letzte Änderung:"
	git --no-pager log --pretty=format:'* [%h] %s' HEAD^..

# last possibility: updated to a newer version
else
	echo "Softwarestand jetzt auf Version [$(git rev-parse --short HEAD)]."
	echo "Änderungen seit letztem Update:"
	git --no-pager log --pretty=format:'* [%h] %s' $OLD_HASH..
fi

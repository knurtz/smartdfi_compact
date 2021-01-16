#!/bin/sh

echo "Content-Type: text/plain"
echo ""

cd /var/www/html
git reset --hard
git pull
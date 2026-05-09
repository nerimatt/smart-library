#!/bin/bash

wipe_flag=false

# https://stackoverflow.com/questions/7069682/how-to-get-arguments-with-flags-in-bash
# while getopts "w" flag; do
#     case "${flag}" in
#         w) wipe_flag=true;;
#
#
#     esac
# done

for arg in "$@"; do
    case "$arg" in
        --wipe) wipe_flag=true;;
    esac
done

if $wipe_flag; then
    echo "wiping first..." && mpremote cp wipe.py : && mpremote run wipe.py
fi

# get files in espignore, ignoring spaces
# pass in other grep with -f to accept these as params
# -x only match whole line
# -v exclude
# -F dont treat strings as regex
files2upload="$(ls | grep -vFxf <(grep -v '^[[:space:]]*$' .espignore))"

mpremote fs cp -r $files2upload :


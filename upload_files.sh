
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

mpremote fs cp -r $(ls | grep -v firmware) :



wipe_flag=false

if [ $# -eq 0 ]
then
    echo "No arguments supplied"
    exit
fi

for arg in "$@"; do
    case "$arg" in
        --wipe) wipe_flag=true;;
    esac
done

if $wipe_flag; then
    echo "wiping first..." && mpremote cp wipe.py : && mpremote run wipe.py
fi

mpremote fs cp -r $1 :


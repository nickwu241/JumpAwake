#/bin/sh
set -x

# usage: <user_id> <seconds_from_now>
curl -X POST --data ''"$(date -u -v+${2}S +'%Y-%m-%dT%H:%M:%SZ')"'' \
    -H 'Content-type: application/json' \
    "http://7fbfdf67.ngrok.io/${1}/alarm"

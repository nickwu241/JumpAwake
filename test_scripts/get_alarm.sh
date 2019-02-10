#/bin/sh
set -x
# usage: <user_id>
curl "http://wakeupthe.net:5000/${1}/alarm"

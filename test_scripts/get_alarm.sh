#/bin/sh
set -x
# usage: <user_id>
curl "localhost:5000/${1}/alarm"

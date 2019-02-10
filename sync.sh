#!/bin/sh

rsync --exclude='motion_detection' --exclude='functions' --filter=':- .gitignore' \
    -ave ssh /Users/nickwu/src/github.com/nickwu241/JumpAwake "$(terraform output ip)":~/

rsync -ave ssh /Users/nickwu/src/github.com/nickwu241/JumpAwake/dist "$(terraform output ip)":~/JumpAwake
rsync -ave ssh /Users/nickwu/src/github.com/nickwu241/JumpAwake/firebase-sa-secret.json "$(terraform output ip)":~/JumpAwake
rsync -ave ssh /Users/nickwu/src/github.com/nickwu241/JumpAwake/gce-sa-secret.json "$(terraform output ip)":~/JumpAwake
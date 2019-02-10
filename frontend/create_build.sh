#!/bin/sh
set -euo pipefail
ORIG_DIR=$(PWD)
SCRIPT_DIR=$(dirname "$0")
(cd $SCRIPT_DIR && npm run build && rm -rf ../dist && mv dist ..) || cd $ORIG_DIR
cd $ORIG_DIR

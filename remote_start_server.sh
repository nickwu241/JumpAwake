#!/bin/sh

ssh $(terraform output ip) 'cd ~/JumpAwake && \
    pipenv install && \
    pipenv run ./start_server.sh'

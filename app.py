#!/usr/bin/env python

from flask import Flask, abort, jsonify, request

import models

app = Flask(__name__)

jump_count = 0

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/<user_id>/jump', methods=['GET', 'POST'])
def jump(user_id):
    if request.method == 'GET':
        return jsonify(models.User(user_id).data)
    elif request.method == 'POST':
        models.User(user_id).increment_jump()
        return jsonify({'status': 'OK'})
    abort(400)

@app.route('/<user_id>/jump/end', methods=['POST'])
def end_jump_session(user_id):
    models.User(user_id).end_jump_session()
    return jsonify({'status': 'OK'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

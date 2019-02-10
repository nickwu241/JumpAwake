#!/usr/bin/env python

from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/jump', method=['POST'])
def jump():
    return 'OK'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

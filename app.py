#!/usr/bin/env python

from flask import Flask, abort, jsonify, request, send_from_directory, render_template
from flask_socketio import SocketIO

import models

app = Flask(__name__, static_folder='dist/static', template_folder='dist')
socketio = SocketIO(app)

clients = {}

# Socket Set Up
def __emit_jumps():
    print('__emit_jumps()')
    socketio.emit('jumps', __get_encoded_client_data())

def __get_encoded_client_data():
    return {c['user']: c['data'] for c in clients.values()}

@socketio.on('join')
def join(user):
    print("[WS] {} connected via join".format(request.sid))
    clients[request.sid] = {
        'user': user,
        'data': models.User(user).data
    }
    if len(clients) >= 2:
        __emit_jumps()

@socketio.on('leave')
def leave(data):
    print("[WS] {} disconnected via leave".format(request.sid))
    clients.pop(request.sid, None)

@socketio.on('connect')
def connect():
    print("[WS] {} connected".format(request.sid))

@socketio.on('disconnect')
def disconnect():
    print("[WS] {} disconnected".format(request.sid))
    clients.pop(request.sid, None)

# Backend Routing
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')

@app.route('/clients')
def show_clients():
    return jsonify(clients)

@app.route('/time_series')
def show_time_series():
    return jsonify(models.get_time_series())

@app.route('/<user_id>/time_series')
def show_user_time_series(user_id):
    return jsonify(models.get_time_series(filter_user_name=user_id))

@app.route('/<user_id>/alarm', methods=['GET', 'POST'])
def user_alarms(user_id):
    if request.method == 'GET':
        return str(models.User(user_id).seconds_until_alarm < 0)
    elif request.method == 'POST':
        models.User(user_id).set_alarm(request.data.decode())
        return jsonify({'status': 'OK'})
    abort(400)

@app.route('/<user_id>/jump', methods=['GET', 'POST'])
def user_jump(user_id):
    if request.method == 'GET':
        return jsonify(models.User(user_id).data)
    elif request.method == 'POST':
        for c in clients.values():
            if c['user'] == user_id:
                c['data']['jumps'] = models.User(user_id).increment_jump()
                break
        else:
            models.User(user_id).increment_jump()

        __emit_jumps()
        return jsonify({'status': 'OK'})
    abort(400)

@app.route('/<user_id>/jump/end', methods=['POST'])
def user_end_jump_session(user_id):
    models.User(user_id).end_jump_session()
    socketio.emit('jumps', 0)
    return jsonify({'status': 'OK'})


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)

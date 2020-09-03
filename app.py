from flask import Flask
from flask import request, url_for, redirect
from flask_cors import CORS
from flask_socketio import SocketIO, emit

import db

app = Flask(__name__, static_url_path='/static', static_folder='static')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on('connect')
def test_connect():
    print('Client Connected')


@socketio.on('disconnect')
def test_disconnect():
    print('Client Disconnected')


@socketio.on('newgame')
def newgame(message):
    id = db.new_game(str(message['board']), request.sid)
    emit('gamecreated', {'gameid': id})


@socketio.on('update')
def update(message):
    db.update_game(message['id'], str(message['board']))
    lastplay = db.get_color_by_sid(message['id'], request.sid)
    if lastplay == 'r':
        nextplay = 'y'
    else:
        nextplay = 'r'
    nextsid = db.get_sid_by_color(message['id'], nextplay)
    if nextsid is not None:
        emit('opponentmove', {'board': message['board']}, room=nextsid)


@socketio.on('joingame')
def joingame(message):
    db.join_game(message['id'], request.sid)
    db.delete_game(message['oldid'])


@socketio.on('endgame')
def endgame(message):
    db.delete_game(message['id'])


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='circle-32.ico'))


if __name__ == '__main__':
    # app.run(debug=True, host='192.168.2.242', port=5000)
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)

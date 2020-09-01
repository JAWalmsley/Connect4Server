from flask import Flask
from flask import request
from flask import jsonify, json
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit

import db

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on('connect')
def test_connect():
    print('Client Connected')
    emit('swag', {'data': 'Swag Moment'})


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
    emit('opponentmove', {'board': message['board']}, room=nextsid)
    print(nextsid)


@socketio.on('joingame')
def joingame(message):
    db.join_game(message['id'], request.sid)


# @app.route('/newgame', methods=['POST'])
# def newgame():
#     board = request.json['board']
#     id = db.new_game(board)
#     response = jsonify({'gameid': id})
#     return response, 201
#
#
# @app.route('/updategame', methods=['POST'])
# def updategame():
#     id = request.json['id']
#     board = request.json['board']
#     board = json.loads(board)
#     print(board)
#     # db.update_game(id, board)
#     response = jsonify({'gameid': id})
#     return response, 200
#
#
# @app.route('/getboard', methods=['POST'])
# @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
# def getboard():
#     id = request.json['id']
#     board = db.get_board(id)
#     response = jsonify({'board': board})
#     return response, 200


if __name__ == '__main__':
    # app.run()
    socketio.run(app)

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, jsonify, request
import time
import json

data = {}


def main():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '5b6db414d4fd764a'
    socketio = SocketIO(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api')
    def api():
        return data

    @socketio.on('connected')
    def connected():
        emit('data', data)

    socketio.run(app, host='0.0.0.0', port=5000, debug=True)


def parse_floor_str(local_elevator, express_elevator):
    if(type(local_elevator) == 'string' and type(express_elevator) == 'string'):
        local_elevator = local_elevator.replace(' ', '')
        express_elevator = express_elevator.replace(' ', '')
        if '+' in local_elevator:
            data.local_elevator.up = True
            local_elevator = local_elevator.replace('+', '')
            data.local_elevator.floor = local_elevator
        elif '-' in local_elevator:
            data.local_elevator.down = False
            local_elevator = local_elevator.replace('-', '')
            data.local_elevator.floor = local_elevator
        else:
            data.local_elevator.up = False
            data.local_elevator.down = False
            data.local_elevator.floor = local_elevator

        if '+' in express_elevator:
            data.express_elevator.up = True
            express_elevator = express_elevator.replace('+', '')
            data.express_elevator.floor = express_elevator
        elif '-' in express_elevator:
            data.express_elevator.down = False
            express_elevator = express_elevator.replace('-', '')
            data.express_elevator.floor = express_elevator
        else:
            data.express_elevator.up = False
            data.express_elevator.down = False
            data.express_elevator.floor = express_elevator

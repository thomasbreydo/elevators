from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, jsonify, request
import time
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = '5b6db414d4fd764a'
socketio = SocketIO(app)

# JSON_NAME = "state.json"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api')
def api():
    return read_file()


@socketio.on('connected')
def connected():
    emit('data', read_file())


def read_file():
    with open(JSON_NAME) as f:
        return json.load(f)


def main(elevator1_position, elevator2_position):
    if(type(elevator1_position) == 'string' and type(elevator2_position) == 'string'):
        socketio.run(app, host='0.0.0.0', port=5000, debug=True)

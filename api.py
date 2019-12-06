from flask_socketio import SocketIO, emit
from flask import Flask, render_template, jsonify, request
import time
import json


data = {
    'local_elevator': {
        'up': False,
        'down': False,
        'floor': '--'
    },
    'express_elevator': {
        'up': False,
        'down': False,
        'floor': '--'
    }
}

app = Flask(__name__)
app.config['SECRET_KEY'] = '5b6db414d4fd764a'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api')
def api():
    global data
    return json.dumps(data)


@app.route('/log')
def log():
    return "This is where the log will be!"


@socketio.on('connected')
def connected():
    global data
    emit('data', json.dumps(data))


def main():
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)


def parse_floors_str(local_elevator, express_elevator):
    global data
    try:
        local_elevator = local_elevator.replace(' ', '')
        express_elevator = express_elevator.replace(' ', '')
        if '+' in local_elevator:
            data['local_elevator']['up'] = True
            data['local_elevator']['down'] = False
            data['local_elevator']['floor'] = local_elevator.replace('+', '')
        elif '-' in local_elevator:
            data['local_elevator']['up'] = False
            data['local_elevator']['down'] = True
            data['local_elevator']['floor'] = local_elevator.replace('-', '')
        else:
            data['local_elevator']['up'] = False
            data['local_elevator']['down'] = False
            data['local_elevator']['floor'] = local_elevator

        if '+' in express_elevator:
            data['express_elevator']['up'] = True
            data['express_elevator']['down'] = False
            data['express_elevator']['floor'] = express_elevator.replace(
                '+', '')
        elif '-' in express_elevator:
            data['express_elevator']['up'] = False
            data['express_elevator']['down'] = True
            data['express_elevator']['floor'] = express_elevator.replace(
                '-', '')
        else:
            data['express_elevator']['up'] = False
            data['express_elevator']['down'] = False
            data['express_elevator']['floor'] = express_elevator

    except:
        print('Error occured in api.py!')


if __name__ == "__main__":
    main()

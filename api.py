from multiprocessing import Process
from flask_socketio import SocketIO, emit
from flask import Flask, render_template
import time
import json
import zmq

context = zmq.Context()

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5001")


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


def listener():
    while True:
        message = socket.recv()
        socketio.emit('data', message, broadcast=True)
        socket.send('Broadcasted')


def main():
    main_listener = Process(target=listener)
    main_listener.start()
    try:
        socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        main_listener.join()


if __name__ == "__main__":
    main()

# data = {
#     'local_elevator': {
#         'up': False,
#         'down': False,
#         'floor': '--'
#     },
#     'express_elevator': {
#         'up': False,
#         'down': False,
#         'floor': '--'
#     }
# }

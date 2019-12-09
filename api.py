from multiprocessing import Process
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, jsonify
import time
import zmq

context = zmq.Context()

api_socket = context.socket(zmq.REQ)
api_socket.connect("tcp://localhost:5001")


app = Flask(__name__)
app.config['SECRET_KEY'] = '5b6db414d4fd764a'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api')
def api():
    api_socket.send(b'Request')
    return jsonify(api_socket.recv())


@app.route('/log')
def log():
    return "This is where the log will be!"


@socketio.on('connected')
def connected():
    emit('data', api_socket.recv())


def listener():
    update_socket = context.socket(zmq.REP)
    update_socket.connect("tcp://localhost:5002")
    while True:
        socketio.emit('data', update_socket.recv(), broadcast=True)
        update_socket.send(b'Recieved')


def main():
    updates_listener = Process(target=listener)
    updates_listener.start()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        updates_listener.join()


if __name__ == "__main__":
    main()

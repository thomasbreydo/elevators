from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO

service_elevator_going_up = True
service_elevator_going_down = True
service_elevator_floor = 12
express_elevator_going_up = True
express_elevator_going_down = True
express_elevator_floor = 12

app = Flask(__name__)
app.config['SECRET_KEY'] = '5b6db414d4fd764a'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html', going_up=service_elevator_going_up)


@app.route('/api')
def api():
    return jsonify(
        service_elevator_going_up=service_elevator_going_up,
        service_elevator_going_down=service_elevator_going_down,
        service_elevator_floor=service_elevator_floor,
        express_elevator_going_up=express_elevator_going_up,
        express_elevator_going_down=express_elevator_going_down,
        express_elevator_floor=express_elevator_floor
    )


@app.route('/hello/<name>')
def hello_name(name):
    return render_template('hello.html', name=name)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

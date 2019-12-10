from multiprocessing import Process
import zmq
import time
import json

current_data = {
    'local_elevator': {
        'up': True,
        'down': True,
        'floor': '--'
    },
    'express_elevator': {
        'up': False,
        'down': False,
        'floor': '--'
    }
}

context = zmq.Context()


def api_listener():
    api_socket = context.socket(zmq.REP)
    api_socket.bind("tcp://*:3001")
    while True:
        message = api_socket.recv()
        if message == b'Request':
            api_socket.send(json.dumps(current_data).encode('utf-8'))
        else:
            api_socket.send('Invalid!')


def updates_listener():
    global current_data
    update_socket = context.socket(zmq.REQ)
    update_socket.bind("tcp://*:3002")
    elevator_socket = context.socket(zmq.REP)
    elevator_socket.bind("tcp://*:3003")
    while True:
        message = elevator_socket.recv()
        elevator_socket.send(b'Recieved!')
        message = message.decode('utf-8')
        message = message.split(';')
        returned_data = parse_floors_str(message[0], message[1], current_data)
        print(returned_data)
        print(current_data)
        if returned_data != current_data:
            current_data = returned_data
            update_socket.send(json.dumps(data).encode('utf-8'))
            update_socket.recv()


def main():
    listener_to_updates = Process(target=updates_listener)
    listener_to_updates.start()
    listener_to_api = Process(target=api_listener)
    listener_to_api.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        listener_to_updates.join()
        listener_to_api.join()


def parse_floors_str(local_elevator, express_elevator, data):
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

        return data

    except:
        print('Error occured in middleware.py!')


if __name__ == "__main__":
    main()

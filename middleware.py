from multiprocessing import Process
import zmq
import time

data = {
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
    api_socket.bind("tcp://*:5001")
    while True:
        message = api_socket.recv()
        print(message)
        if message == b'Request':
            api_socket.send(str(data).encode('utf-8'))
        else:
            api_socket.send('Invalid!')


def updates_listener():
    update_socket = context.socket(zmq.REQ)
    update_socket.bind("tcp://*:5002")
    elevator_socket = context.socket(zmq.REP)
    elevator_socket.bind("tcp://*:5003")
    while True:
        message = cv2_socket.recv()
        cv2_socket.send(b'Recieved!')
        message = message.split(';')
        returned_data = parse_floors_str(message[0], message[1], data)
        if returned_data != data:
            data = returned_data
        api_socket.send(str(data).encode('utf-8'))
        api_socket.recv()


def main():
    forward_updates_listener = Process(target=forward_updates)
    forward_updates_listener.start()
    listener_to_api = Process(target=api_listener)
    listener_to_api.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        forward_updates_listener.join()
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

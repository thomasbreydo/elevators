import zmq


def main():
    context = zmq.Context()
    cv2_socket = context.socket(zmq.REP)
    cv2_socket.bind("tcp://*:5002")
    api_socket = context.socket(zmq.REP)
    api_socket.bind("tcp://*:5001")
    while True:
        print('Waiting...!')
        message = socket.recv()
        socket.send(b"Recieved!")
        print(message)


def parse_floors_str(local_elevator, express_elevator):
        # global data
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
        print('Error occured in middleware.py!')


if __name__ == "__main__":
    main()

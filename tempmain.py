from multiprocessing import Process
import api
import time


def main():
    while True:
        time.sleep(5)
        api.parse_floors_str(' + 1 3', ' -  12')
        print('api!')


if __name__ == "__main__":
    Process(target=api.main).start()
    Process(target=main).start()

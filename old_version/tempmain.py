from multiprocessing import Process, Pipe
import api
import time
import random

parent_pipe, child_pipe = Pipe()


def main():
    while True:
        time.sleep(2)
        parent_pipe.send([' + ' + str(random.randint(0, 14)),
                          ' -  ' + str(random.randint(0, 14))])
        print('Api!')


if __name__ == "__main__":
    parent_pipe, child_pipe = Pipe()
    Process(target=api.main, args=(child_pipe,)).start()
    main()

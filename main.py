from multiprocessing import Process
import middleware as mw
# import camera_main as cm
import api
import time


def main():
    main_mw = Process(target=mw.main)
    main_mw.start()
    # main_camera = Process(target=cm.main)
    # main_camera.start()
    main_api = Process(target=api.main)
    main_api.start()

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        main_api.join()
        # main_camera.join()
        main_mw.join()


if __name__ == "__main__":

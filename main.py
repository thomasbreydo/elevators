import camera
import cv2
import parser

WAITKEY_DELAY = 1  # ms
STOP_CHAR = 'q'
PORT = 0  # if reading from file, set PORT to the video's path

#  DEBUG
NUM_WARMUP = 0
WINDOW_NAME = 'Video Stream'
SCREEN_HEIGHT = 900
SCREEN_WIDTH = 1440


def was_not_stopped():
    return cv2.waitKey(WAITKEY_DELAY) != ord(STOP_CHAR)


def main():
    with camera.GetCamera(PORT) as cam:
        # DEBUG
        cam.warm_up(NUM_WARMUP)

        while was_not_stopped():
            image = cam.capture()
            rotated = cv2.rotate(image, cv2.ROTATE_180)
            parser = parser.ElevatorParser(rotated)

            # DEBUG


if __name__ == "__main__":
    main()

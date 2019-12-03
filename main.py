import camera
import cv2
import logger
import parse

WAITKEY_DELAY = 1  # ms
STOP_CHAR = 'q'

PORT = 0  # if reading from file, set PORT to the video's path
NUM_WARMUP = 75

LOG = False

SHOW = True
WINDOW_NAME = 'Video Stream'


def was_not_stopped():
    return cv2.waitKey(WAITKEY_DELAY) != ord(STOP_CHAR)


def main():
    with camera.GetCamera(PORT) as cam:
        if type(PORT) == 'int':  # don't warm up if from file
            cam.warm_up(NUM_WARMUP)

        while was_not_stopped():
            image = cam.capture()
            if SHOW:
                cv2.imshow(WINDOW_NAME, image)
            parser = parse.DigitParser(image)
            panels = parser.parse()
            if LOG:
                logger.log(panels)


if __name__ == "__main__":
    main()

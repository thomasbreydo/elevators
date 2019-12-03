import camera
import cv2
import logger
import parse

WAITKEY_DELAY = 1  # ms
STOP_CHAR = 'q'

PORT = 0  # if reading from file, set PORT to the video's path
NUM_WARMUP = 75

LOG = True

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
            cv2.imshow(WINDOW_NAME, image)
            parser = parse.DigitParser(image)
            for panel_str in parser.parse():
                print(panel_str, end=',')

            # if LOG:
            #     logger.log(numbers)
            # if SHOW:
            #     # ADD ~draw bboxes on image FUNCTIONALITY
            #     cv2.imshow(WINDOW_NAME, image)


if __name__ == "__main__":
    main()

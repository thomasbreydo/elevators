import camera
import cv2
import logger
import parse
import panels

WAITKEY_DELAY = 1  # ms
STOP_CHAR = 'q'

PORT = 0  # if reading from file, set PORT to the video's path
NUM_WARMUP = 0

LOG = False

SHOW = True
WINDOW_NAME = 'Video Stream'
SCREEN_HEIGHT = 1440
SCREEN_WIDTH = 2304


def was_not_stopped():
    return cv2.waitKey(WAITKEY_DELAY) != ord(STOP_CHAR)


def main():
    with camera.GetCamera(PORT) as cam:
        if type(PORT) == 'int':  # don't warm up if from file
            cam.warm_up(NUM_WARMUP)

        while was_not_stopped():
            image = cam.capture()
            image = cv2.rotate(image, cv2.ROTATE_180)
            parser = panels.Corners(image)
            parser.set_corners()
            parser.reduce_corners()
            floors = []

            if LOG:
                logger.log(floors)
            if SHOW:
                image_plain = cv2.resize(
                    image.copy(), ((SCREEN_WIDTH//4, SCREEN_HEIGHT//4)))

                # marked = parser.binary.copy()
                # for bbox in parser.panel_bboxes:
                #     marked = cv2.rectangle(
                #         marked, (bbox[2], bbox[0]), (bbox[3], bbox[1]), (0, 255, 0))
                # marked = cv2.resize(
                #     marked, (SCREEN_WIDTH//4, SCREEN_HEIGHT//4))

                binary = cv2.resize(
                    parser.binary.copy(), (SCREEN_WIDTH//4, SCREEN_HEIGHT//4))

                with_corners = image.copy()
                for pt in parser.corners:
                    cv2.circle(with_corners, tuple(
                        reversed(pt)), 3, (0, 0, 255), -1)
                with_corners = cv2.resize(
                    with_corners, (SCREEN_WIDTH//4, SCREEN_HEIGHT//4))

                cv2.imshow(WINDOW_NAME + ' - Plain', image_plain)
                cv2.imshow(WINDOW_NAME + ' - Binary', binary)
                # cv2.imshow(WINDOW_NAME + '3', marked)
                cv2.imshow(WINDOW_NAME + ' - Corners', with_corners)
            print(','.join(floors))


if __name__ == "__main__":
    main()

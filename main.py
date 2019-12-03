import camera
import cv2
import logger
import parse
import panels

WAITKEY_DELAY = 1  # ms
STOP_CHAR = 'q'

PORT = 0  # if reading from file, set PORT to the video's path
NUM_WARMUP = 15

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
            parser = panels.Corners(image)
            parser.set_corners()
            parser.reduce_corners()

            if LOG:
                logger.log(panels)
            if SHOW:
                image_plain = cv2.resize(
                    image.copy(), ((SCREEN_WIDTH//4, SCREEN_HEIGHT//4)))

                marked = parser.binary.copy()
                for bbox in parser.panel_bboxes:
                    marked = cv2.rectangle(
                        marked, (bbox[2], bbox[0]), (bbox[3], bbox[1]), (0, 255, 0))
                marked = cv2.resize(
                    marked, (SCREEN_WIDTH//4, SCREEN_HEIGHT//4))

                binary = cv2.resize(
                    parser.binary.copy(), (SCREEN_WIDTH//4, SCREEN_HEIGHT//4))

                corner_points = image.copy()
                for pt in parser.coor_tuples:
                    cv2.circle(corner_points, tuple(
                        reversed(pt)), 3, (0, 0, 255), -1)
                corner_points = cv2.resize(
                    corner_points, (SCREEN_WIDTH//4, SCREEN_HEIGHT//4))

                cv2.imshow(WINDOW_NAME + '1', image_plain)
                cv2.imshow(WINDOW_NAME + '2', binary)
                cv2.imshow(WINDOW_NAME + '3', marked)
                cv2.imshow(WINDOW_NAME + '4', corner_points)
            print(','.join(panels))


if __name__ == "__main__":
    main()

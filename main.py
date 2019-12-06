from multiprocessing import Process
import camera
import cv2
import parser
import api

WAITKEY_DELAY = 1  # ms
STOP_CHAR = 'q'
PORT = 0  # if reading from file, set PORT to the video's path

# ymin, ymax, xmin, xmax
PANEL1 = (239, 390, 38, 500)
PANEL2 = (10, 100, 108, 225)


def was_not_stopped():
    return cv2.waitKey(WAITKEY_DELAY) != ord(STOP_CHAR)


def main():
    with camera.GetCamera(PORT) as cam:

        while was_not_stopped():
            # image
            image = cam.capture()

            # crop panels
            top = image[PANEL1[0]: PANEL1[1],
                        PANEL1[2]: PANEL1[3]]
            bottom = image[PANEL2[0]: PANEL2[1],
                           PANEL2[2]: PANEL2[3]]

            # rotate
            rotated_top = cv2.rotate(top, cv2.ROTATE_90_COUNTERCLOCKWISE)
            rotated_bottom = cv2.rotate(bottom, cv2.ROTATE_90_COUNTERCLOCKWISE)

            # parse
            # parser_top = parser.ElevatorParser(rotated_top)
            # parser_bottom = parser.ElevatorParser(rotated_bottom)
            # elevator1 = parser_top.parse()
            # elevator2 = parser_bottom.parse()

            # display
            cv2.imshow('ELEVATOR1', rotated_top)
            cv2.imshow('ELEVATOR2', rotated_bottom)


if __name__ == "__main__":
    main()
    # Process(target=main).start()
    # Process(target=api.main, args=(ELEVATOR1, ELEVATOR2)).start()

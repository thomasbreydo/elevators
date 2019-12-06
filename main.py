from multiprocessing import Process
import camera
import cv2
import parser
import api

WAITKEY_DELAY = 1  # ms
STOP_CHAR = 'q'
PORT = 0  # if reading from file, set PORT to the video's path

# ymin, ymax, xmin, xmax
ARROW1 = (647, 671, 740, 779)
ARROW2 = (646, 670, 812, 845)
FLOOR1 = (577, 644, 741, 777)
FLOOR2 = (574, 644, 809, 848)


def was_not_stopped():
    return cv2.waitKey(WAITKEY_DELAY) != ord(STOP_CHAR)


def main():
    with camera.GetCamera(PORT) as cam:

        while was_not_stopped():
            # image
            image = cam.capture()

            # crop panels
            arrow1 = image[ARROW1[0]: ARROW1[1],
                           ARROW1[2]: ARROW1[3]]
            arrow2 = image[ARROW2[0]: ARROW2[1],
                           ARROW2[2]: ARROW2[3]]
            floor1 = image[FLOOR1[0]: FLOOR1[1],
                           FLOOR1[2]: FLOOR1[3]]
            floor2 = image[FLOOR2[0]: FLOOR2[1],
                           FLOOR2[2]: FLOOR2[3]]

            # rotate
            rotated_arrow1 = cv2.rotate(arrow1, cv2.ROTATE_90_CLOCKWISE)
            rotated_arrow2 = cv2.rotate(arrow2, cv2.ROTATE_90_CLOCKWISE)
            rotated_floor1 = cv2.rotate(floor1, cv2.ROTATE_90_CLOCKWISE)
            rotated_floor2 = cv2.rotate(floor2, cv2.ROTATE_90_CLOCKWISE)

            # parse
            parser_arrow1 = parser.ElevatorParser(rotated_arrow1)
            parser_arrow2 = parser.ElevatorParser(rotated_arrow2)
            parser_floor1 = parser.ElevatorParser(rotated_floor1)
            parser_floor2 = parser.ElevatorParser(rotated_floor2)

            elevator1 = parser_arrow1.parse() + parser_floor1.parse()
            elevator2 = parser_arrow2.parse() + parser_floor2.parse()

            # display
            cv2.imshow('ARROW1', rotated_arrow1)
            cv2.imshow('ARROW2', rotated_arrow2)
            cv2.imshow('FLOOR1', rotated_floor1)
            cv2.imshow('FLOOR2', rotated_floor2)

            print('\n\n')
            print(elevator1)
            print(elevator2)


if __name__ == "__main__":
    Process(target=main).start()
    Process(target=api.main).start()

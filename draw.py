import numpy as np
import cv2
import camera

WAITKEY_DELAY = 1
STOP_CHAR = 'q'
IMAGEPATH = 'tests/test.jpg'

corner1 = (0, 0)
corner2 = (0, 0)


def was_not_stopped():
    return cv2.waitKey(WAITKEY_DELAY) != ord(STOP_CHAR)


def update_corners(event, x, y, flags, param):
    global corner1, corner2
    if event == cv2.EVENT_LBUTTONDOWN:
        corner1 = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        corner2 = (x, y)


cv2.namedWindow('image')
cv2.setMouseCallback('image', update_corners)

while was_not_stopped():


cv2.destroyAllWindows()

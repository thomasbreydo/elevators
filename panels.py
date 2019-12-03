# import the necessary packages
import cv2
import math
import numpy as np

AREA_THRESHOLD = 500
ASPECT_RATIO_THRESHOLD = 2.5
BINARY_THRESHOLD = 30
DIST_THRESH = 50

PERIMETER_SCALAR = 0.1

GAUSSIAN_KERNEL = (5, 5)

CORNER_ARGS = [2, 3, 0.04]
CORNER_THRESH = 0.1  # lower for more corners detected


class PanelDetector:
    def __init__(self, image):
        self.image = image

    def is_panel(self, contour):
        '''Return bbox if ``contour`` matches panel criteria.'''
        # approximate a polygon
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, PERIMETER_SCALAR * perimeter, True)

        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            if w * h >= AREA_THRESHOLD and w / h >= ASPECT_RATIO_THRESHOLD:
                return (y, y + h, x, x + w)  # ymin, ymax, xmin, xmax

    def get_contours(self):
        '''Return all contours.'''
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        # blurred = cv2.GaussianBlur(gray, GAUSSIAN_KERNEL, 0)
        blurred = cv2.bilateralFilter(gray, 5, 75, 75)
        _, binary = cv2.threshold(
            blurred, BINARY_THRESHOLD, 255, cv2.THRESH_BINARY)

        self.binary = binary

        # corners = cv2.cornerHarris(blurred, 2, 3, 0.04)

        contours, _ = cv2.findContours(binary.copy(), cv2.RETR_TREE,
                                       cv2.CHAIN_APPROX_NONE)
        return contours

    def get_panels(self):
        '''Return list of boudning boxes that match panel criteria.

        Bounding boxes are returned in a sorted list, highest bounding box
        in the image appears first.
        '''
        contours = self.get_contours()
        panels_bboxes = []
        for contour in contours:
            bbox = self.is_panel(contour)
            if bbox is not None:
                panels_bboxes.append(bbox)
        # sort by smallest ymin
        panels_bboxes.sort(key=lambda x: x[0])
        self.panel_bboxes = panels_bboxes
        return panels_bboxes


class Corners:
    def __init__(self, image):
        self.image = image

    def set_corners(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        # blurred = cv2.GaussianBlur(gray, GAUSSIAN_KERNEL, 0)
        blurred = cv2.bilateralFilter(gray, 5, 75, 75)
        _, binary = cv2.threshold(
            blurred, BINARY_THRESHOLD, 255, cv2.THRESH_BINARY)

        self.binary = binary

        dst = cv2.cornerHarris(blurred, *CORNER_ARGS)
        mask = np.zeros_like(gray)
        mask[dst > CORNER_THRESH*dst.max()] = 255
        coordinates = np.argwhere(mask)

        self.corners = [tuple(l) for l in [l.tolist()
                                           for l in list(coordinates)]]

    def distance(self, pt1, pt2):
        (x1, y1), (x2, y2) = pt1, pt2
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def reduce_corners(self):
        coor_tuples_copy = self.corners
        i = 1
        for pt1 in self.corners:
            for pt2 in self.corners[i::1]:
                if(self.distance(pt1, pt2) < 50):
                    coor_tuples_copy.remove(pt2)
            i += 1

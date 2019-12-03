# import the necessary packages
import cv2

AREA_THRESHOLD = 500
ASPECT_RATIO_THRESHOLD = 2.5
BINARY_THRESHOLD = 50

GAUSSIAN_KERNEL = (5, 5)


class PanelDetector:
    def __init__(self, image):
        self.image = image

    def is_panel(self, contour):
        '''Return bbox if ``contour`` matches panel criteria.'''
        # approximate a polygon
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)

        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            if w * h >= AREA_THRESHOLD and w / h >= ASPECT_RATIO_THRESHOLD:
                return (y, y + h, x, x + w)  # ymin, ymax, xmin, xmax

    def get_contours(self):
        '''Return all contours.'''
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, GAUSSIAN_KERNEL, 0)
        _, binary = cv2.threshold(
            blurred, BINARY_THRESHOLD, 255, cv2.THRESH_BINARY)

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
        return panels_bboxes

import cv2

BI_FILTER_ARGS = [5, 75, 75]
BINARY_THRESH = 30
CORNER_ARGS = [2, 3, 0.04]


class ElevatorParser:
    def __init__(self, image):
        self.original_image = image
        self.gray_image = cv2.cvtColor(
            self.original_image, cv2.COLOR_BGR2GRAY)
        self.blurred_image = cv2.bilateralFilter(
            self.gray_image, *BI_FILTER_ARGS)

        # DEBUG
        self.binary_image = cv2.threshold(
            self.blurred_image, BINARY_THRESH, 255, cv2.THRESH_BINARY)

    def _get_corners(self):
        dst = cv2.cornerHarris(blurred, *CORNER_ARGS)

    def _warp_perspective(self, corners):
        pass

    def _get_bboxes(self):
        corners = self._get_corners()

    def parse(self):
        floors = []
        for bbox in self.get_bboxes():
            cropped = self.image[bbox[0]: bbox[1], bbox[2]: bbox[3]]
            floors.append(ptt.image_to_string(
                cropped, lang="arrowsplusminus+segment",
                config='-c tessedit_char_whitelist=0123456789+- '
                + '--psm 7 --oem 3'))
        return floors

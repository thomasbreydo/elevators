import os
import cv2
import pytesseract as ptt
import panels


class DigitParser(panels.PanelDetector):
    def parse(self):
        for bbox in self.get_panels():
            cropped = self.image[bbox[0]: bbox[1], bbox[2]: bbox[3]]
            yield ptt.image_to_string(
                cropped, lang="arrowsplusminus+segment",
                config='-c tessedit_char_whitelist=0123456789+- --psm 7 --oem 3')   # --psm 5 --oem 3

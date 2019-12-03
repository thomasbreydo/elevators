import os
import pytesseract as ptt
import panels


class DigitParser(panels.PanelDetector):
    def parse(self):
        floors = []
        for bbox in self.get_panels():
            cropped = self.image[bbox[0]: bbox[1], bbox[2]: bbox[3]]
            floors.append(ptt.image_to_string(
                cropped, lang="arrowsplusminus+segment",
                config='-c tessedit_char_whitelist=0123456789+- '
                + '--psm 7 --oem 3'))
        return floors

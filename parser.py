import pytesseract as ptt


class ElevatorParser:
    def __init__(self, image):
        self.image = image

    def parse(self):
        return ptt.image_to_string(
            self.image, lang="arrowsplusminus+segment",
            config='-c tessedit_char_whitelist=0123456789+- '
            + '--psm 7 --oem 3')

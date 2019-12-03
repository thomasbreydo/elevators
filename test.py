import parse
import cv2
import pytesseract as ptt

TESTDIR = 'tests'

image = cv2.VideoCapture(f'{TESTDIR}/temp.jpg')

parser = parse.DigitParser(image)
for panel_str in parser.parse():
    print(panel_str)

import parse
import cv2
import os
import time

TESTDIR = 'tests'
TESTIMG = 'test.jpg'

image = cv2.imread(os.path.join(TESTDIR, TESTIMG))

parser = parse.DigitParser(image)

for panel_str in parser.parse():
    print(panel_str)

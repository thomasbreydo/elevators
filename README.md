# Elevators

A python project that will be able to run on a computer to get the video feed of a webcam, do some image processing on it to get the floor display, and then passing it into tesseract-ocr to recgonize what floor it is on.

## Requirements

1. This project requires Python 3.0 or later and a working installation of pip
2. Basic knowledge of Python

## Notes

1. The arrows.traineddata returns '+' for an up arrow and '-' for a down arrow.

## Installation

1. Follow the Tesseract OCR installation instructions below for your platform.
2. Move the "arrows.traineddata" and "segment.traineddata" files from the traineddata directory into the language directory for Tesseract. If you need more help with that Google some instructions.
3. Install all the requirements from the pip requirements file - could be done with 'pip install -r requirements.txt' in the directory with the requirements file in it.

## Tesseract OCR Installation

### Mac OSX

You can install Tesseract using either MacPorts or Homebrew.

#### Homebrew

```bash
brew install tesseract
```

#### MacPorts

```bash
sudo port install tesseract
```

### Linux

```bash
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
```

## Todos

- [ ] Test the project with the webcam
- [ ] Determine if image warping/tilt is necessary
- [ ] Rename the files, functions, and classes to something more readable
- [ ] Package all the files into a wheel for production
- [ ] Add a Flask server that serves the information as an api
- [ ] Find a location for the Raspberry Pi and the camera
- [ ] Deploy to a Raspberry Pi

import cv2

DEFAULT_PORT = 0


class CustomVideoCapture(cv2.VideoCapture):
    def capture(self):
        return self.read()[1]


class GetCamera:
    def __init__(self, port=DEFAULT_PORT):
        self.port = port

    def __enter__(self):
        self.cam = CustomVideoCapture(self.port)
        return self.cam

    def __exit__(self, type, value, traceback):
        self.cam.release()

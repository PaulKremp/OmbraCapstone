from deepface.detectors import FaceDetector

import cv2

# Not detector because I don't want conflicts in class name
class Recognizer:

    def __init__(self, backend):
        self.backend = backend
        self.recognizer = Recognizer.build_model(backend)


from deepface.detectors import FaceDetector
from deepface import DeepFace

import cv2

# Not detector because I don't want conflicts in class name
class Recognizer:

    def __init__(self, backend):
        self.backend = backend
        self.recognizer = DeepFace.build_model(backend)

    def recognizeFaces(self, faces):

        pass


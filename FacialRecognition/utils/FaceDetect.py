from deepface.detectors import FaceDetector

class FaceDetect:

    def __init__(self, backend):
        self.detector = FaceDetector.build_model(backend)

    def detectFaces(self, image):

        pass

from deepface.detectors import FaceDetector

import cv2
import time

# Not detector because I don't want conflicts in class name
class FaceDetect:

    def __init__(self, backend):
        self.backend = backend
        self.detector = FaceDetector.build_model(backend)

    def detectFaces(self, image) -> list:
        """Returns faces from an image as list [(face, (x, y, w, h)), (face, (x, y, w, h)), ...]
        Args:
            image: OpenCV image (numpy array)

        Returns:
            faces: Faces detected from image
        
        """
        faces = FaceDetector.detect_faces(FaceDetector, self.backend, image)

        for face, (x, y, w, h) in faces:
            faces.append((x, y, w, h))
      
        faces = []
        try:
            faces = FaceDetector.detect_faces(self.detector, self.backend, image)
        except:
            pass
        return faces


    def displayFaces(self, image):
        
        """Displaces faces that are detected from the detector
        Args:
            image: OpenCV image (numpy array)

        Returns:
            keyPress: Key press from the cv2 window 
        
        """
        outputImg = image.copy()
        cv2.rectangle(outputImg, (x, y), (x + w, y + h), (255, 0, 0), 5)


        faces = self.detectFaces(image)
        displayIm = image.copy()
        for face, (x, y, w, h) in faces:
            cv2.rectangle(displayIm, (x, y), (x + w, y + h), (255, 0, 0), 3)
        cv2.imshow("Faces", displayIm)
        keyPress = cv2.waitKey(5)
        return keyPress
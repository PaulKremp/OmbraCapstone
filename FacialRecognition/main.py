from utils.faceDetect import FaceDetect
from utils.recognizer import Recognizer

import cv2

def main():

    # TODO Put everything together (Embedding Creator, FaceDetect, Recognizer)

    faceDetector = FaceDetect("opencv")
    faceRecognizer = Recognizer("VGG-Face")

    cap = cv2.VideoCapture(0)

    while 1:
        ret, img = cap.read()
        if not ret:
            break
        faces = faceDetector.detectFaces(img)



    pass

if __name__ == "__main__":
    
    main()
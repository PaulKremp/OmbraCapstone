from utils import FaceDetect, Recognizer

import cv2

def main():

    # TODO Put everything together (Embedding Creator, FaceDetect, Recognizer)

    faceDetector = FaceDetect("mediapipe")

    cap = cv2.VideoCapture(0)

    while 1:
        ret, img = cap.read()
        if not ret:
            break
        keyPress = faceDetector.displayFaces(img)
        if keyPress == ord("q"):
            cv2.destroyAllWindows()
            break

if __name__ == "__main__":
    
    main()
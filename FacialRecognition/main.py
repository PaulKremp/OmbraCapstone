from utils import EmbeddingGen, FaceDetect, Recognizer

import cv2
import time


def main():

    # TODO Put everything together (Embedding Creator, FaceDetect, Recognizer)

    recognizerBackend = "VGG-Face"
    faceDetectorBackend = "opencv"

    embeddings = EmbeddingGen(
        "./db", recognizerBackend).outputEmbeddings(faceDetectorBackend)
    faceDetector = FaceDetect(faceDetectorBackend)
    faceRecognizer = Recognizer(
        recognizerBackend, embeddings, faceDetectorBackend)

    cap = cv2.VideoCapture(0)

    while 1:
        start_time = time.time()
        ret, img = cap.read()
        if not ret:
            break
        faces = faceDetector.detectFaces(img)
        keyPress = faceRecognizer.displayRecognizedFaces(faces, 0.2, img)
        captureFaces = faceRecognizer.displayCaptureImageFace(faces, 0.2, img)
        
        if keyPress == ord("q"):
            cv2.destroyAllWindows()
            break
        
        print(f"FPS: {1 / (time.time() - start_time)}")


if __name__ == "__main__":

    main()

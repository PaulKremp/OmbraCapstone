from utils import EmbeddingGen, FaceDetect, Recognizer

import cv2
import time
import shutil
import os

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

    # Create directories for recognizedFaces and unrecognizedFaces
    if not os.path.exists("captureImages/recognizedFaces"):
        os.makedirs("captureImages/recognizedFaces")
    if not os.path.exists("captureImages/unrecognizedFaces"):
        os.makedirs("captureImages/unrecognizedFaces")
    
    while 1:
        start_time = time.time()
        ret, img = cap.read()
    
        if not ret:
            break
        faces = faceDetector.detectFaces(img)
        keyPress = faceRecognizer.displayRecognizedFaces(faces, 0.2, img)
        captureImage = faceRecognizer.displayCaptureImageFace(faces, 0.2, img)

       # keyPress to delete the unrecognized and recognized face files within captureImages
        if keyPress == ord("r"):
            # Delete contents of recognizedFaces and unrecognizedFaces directories
            shutil.rmtree("captureImages/recognizedFaces", ignore_errors=True)
            shutil.rmtree("captureImages/unrecognizedFaces", ignore_errors=True)

            # Create recognizedFaces and unrecognizedFaces directories
            os.makedirs("captureImages/recognizedFaces")
            os.makedirs("captureImages/unrecognizedFaces")
        

        if keyPress == ord("q"):
            cv2.destroyAllWindows()
            break
        
        print(f"FPS: {1 / (time.time() - start_time)}")


if __name__ == "__main__":

    main()

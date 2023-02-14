from deepface import DeepFace
from deepface.commons import functions, distance as dst
from datetime import datetime
import cv2
import pandas as pd
import os


class Recognizer:

    def __init__(self, model_name, embeddings, backend):
        self.detector_backend = backend
        self.embeddings = embeddings
        self.model = DeepFace.build_model(model_name)
        self.input_shape = functions.find_input_shape(self.model)

    def recognizeFaces(self, img, faces, threshold):
        """recognizes faces that are detected from the detector
        Args:
            faces: faces detected from the image

            img: OpenCV image (numpy array)

            threshold: 

        Returns:
            recognized_faces: List of recognized faces [(Name, (x, y, w, h), ...)]

        """
        df = pd.DataFrame(self.embeddings, columns=['employee', 'embedding'])

        raw_img = img.copy()
        input_shape_x = self.input_shape[0]
        input_shape_y = self.input_shape[1]

        recognized_faces = []
        
        unrecognized_faces = []

        for face, (x, y, w, h) in faces:
            custom_face = raw_img.copy()[y:y+h, x:x+w]
            custom_face = functions.preprocess_face(img=custom_face, target_size=(
                input_shape_y, input_shape_x), enforce_detection=False, detector_backend=self.detector_backend)
            if custom_face.shape[1:3] == self.input_shape:
                img1_representation = self.model.predict(custom_face)[0, :]
                distances = df.apply(lambda x: dst.findCosineDistance(
                    x['embedding'], img1_representation), axis=1)
                df['distance'] = distances
                df = df.sort_values(by=["distance"])
                candidate = df.iloc[0]
                employee_name = candidate['employee']
                best_distance = candidate['distance']
                if best_distance < threshold:
                    recognized_faces.append((employee_name, (x, y, w, h)))
                else:
                    unrecognized_faces.append((x, y, w, h))
                
        return recognized_faces, unrecognized_faces

    def displayRecognizedFaces(self, faces, threshold, image):
        """displays recognized faces that are detected from the detector
        Args:
            faces: faces detected from the image

            threshold: 

            image: OpenCV image (numpy array)


        Returns:
            keyPress: Key press from the cv2 window 

        """

        reconized_faces, unrecognized_faces = self.recognizeFaces(image, faces, threshold)
        display_im = image.copy()
        for face in reconized_faces:
            name, (x, y, w, h) = face
            cv2.rectangle(display_im, (x, y), (x + w, y + h), (255, 0, 0), 3)
            cv2.putText(display_im, name.split("/")[2], (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0),2)

        for face in unrecognized_faces:
            (x, y, w, h) = face
            cv2.rectangle(display_im, (x, y), (x + w, y + h), (0, 0, 255), 3)
            cv2.putText(display_im, "Unidentified Person", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("Faces", display_im)
        keyPress = cv2.waitKey(5)
        return keyPress


    def displayCaptureImageFace(self, faces, threshold, image):
        """displays capture image of unrecognized and recognized faces that are detected from the detector
            and stores the capture images into a file names "captureImages"
        Args:
            faces: faces detected from the image

            threshold: 

            image: OpenCV image (numpy array)

        Returns:
            recognized_faces_images: capture images of recognized faces 
            unrecognized_faces_images: capture images of unrecognized faces 

        """
            
        reconized_faces, unrecognized_faces = self.recognizeFaces(image, faces, threshold)
        recognized_faces_images = []
        for i, face in enumerate(reconized_faces):
            name, (x, y, w, h) = face
            recognized_face_image = image[y:y+h, x:x+w]
            recognized_face_image = cv2.resize(recognized_face_image, (0,0), fx=2, fy=2)
            recognized_faces_images.append((name.split("/")[2], recognized_face_image))
            current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            cv2.putText(recognized_face_image, "Matched: " + name.split("/")[2] + current_time, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            
            cv2.imwrite('captureImages/recognized_{}_{}.jpg'.format(i, current_time), recognized_face_image )

        unrecognized_faces_images = []
        for i, face in enumerate(unrecognized_faces):
            (x, y, w, h) = face
            unrecognized_face_image = image[y:y+h, x:x+w]
            unrecognized_face_image = cv2.resize(unrecognized_face_image, (0,0), fx=2, fy=2)
            unrecognized_faces_images.append(("Unidentified Person", unrecognized_face_image))
            current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            cv2.putText(unrecognized_face_image, "Unknown: " + current_time, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            
            cv2.imwrite('captureImages/unrecognized_{}_{}.jpg'.format(i, current_time), unrecognized_face_image )

        return recognized_faces_images, unrecognized_faces_images
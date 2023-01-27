from deepface import DeepFace
from deepface.commons import functions, distance as dst

import cv2
import pandas as pd


class Recognizer:

    def __init__(self, model_name, embeddings, backend):
        self.detector_backend = backend
        self.embeddings = embeddings
        self.model = DeepFace.build_model(model_name)
        self.input_shape = functions.find_input_shape(self.model)

    def recognizeFaces(self, img, faces, threshold):
        """recognizes faces that are detected from the detector
        Args:
            faces: 

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

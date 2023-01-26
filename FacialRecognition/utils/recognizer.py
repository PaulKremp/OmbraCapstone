from deepface.detectors import FaceDetector
from deepface import DeepFace
from deepface.commons import functions, distance as dst

import cv2

# Not detector because I don't want conflicts in class name
class Recognizer:

    def __init__(self, model_name, embeddings, input_shape):
        #self.backend = backend
        #self.recognizer = DeepFace.build_model(backend)
        self.embeddings = embeddings
        self.input_shape = input_shape
        self.model = model_name
        # distance metric?

    
    def recognizeFaces(self, faces):
        """recognizes faces that are detected from the detector
        Args:
            faces: 

        Returns:
            detected_faces: 
        
        """
        detector_backend = "opencv"
        faceDetector = FaceDetector.build_model(detector_backend)

        input_shape = functions.find_input_shape(self.detector)
        input_shape_x = input_shape[0]
        input_shape_y = input_shape[1]

        custom_face = raw_img.copy()[y:y+h, x:x+w]
        custom_face = functions.preprocess_face(img=custom_face, target_size=(
        input_shape_y, input_shape_x), enforce_detection=False, detector_backend='opencv')
        threshold = dst.findThreshold(self.model, 'cosine')
        
        # preprocess_face returns single face. this is expected for source images in db.
        img = functions.preprocess_face(img, target_size=(input_shape_y, input_shape_x), enforce_detection=False, detector_backend=detector_backend)
        raw_img = img.copy()
        outputImg = img.copy()
        resolution_x = img.shape[1]
        resolution_y = img.shape[0]
        detected_faces = []

        for face, (x, y, w, h) in faces:
            if custom_face.shape[1:3] == input_shape:
                img1_representation = self.detector.predict(custom_face)[0, :]
                distances = df.apply(lambda x: dst.findCosineDistance(x['embedding'], img1_representation), axis=1)
                df['distance'] = distances
                df = df.sort_values(by=["distance"])
                candidate = df.iloc[0]
                employee_name = candidate['employee']
                best_distance = candidate['distance']
                if best_distance < threshold:
                    detected_faces.append((x, y, w, h, employee_name))
        return detected_faces


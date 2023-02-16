from deepface import DeepFace
from deepface.commons import functions, distance as dst
from deepface.detectors import FaceDetector
from tqdm import tqdm

import os
import pickle


class EmbeddingGen:

    def __init__(self, db_path, model_name):
        self.db_path = db_path
        self.model = model_name

    def loadEmbeddings(self, modelname):
        """loads embeddings using the model name to sort
        Args:
            Model Name

        Returns:
            return embedding based upon model name

        """

        embeddings = []
        if os.path.exists("./db/embeddings_%s.pkl" % modelname):
            f = open("./db/embeddings_%s.pkl" % modelname, "rb")
            embeddings = pickle.load(f)

        return embeddings

    def outputEmbeddings(self, faceDetectorBackend):
        """Check if embedding exists through load embedding function and if not create embedding and load
        Args:
            modelName: Name of face detector name

        Returns:
            embeddings: 

        """
        embeddings = []
        if embeddings := self.loadEmbeddings(self.model):
            pass
        else:
            embeddings = self.createEmbeddings(faceDetectorBackend)
        return embeddings

    def createEmployees(self, db_path):

        employees = []
        if os.path.isdir(db_path) == True:
            for r, d, f in os.walk(db_path):  # r=root, d=directories, f = files
                for file in f:
                    if ('.jpg' in file):
                        # exact_path = os.path.join(r, file)
                        exact_path = r + "/" + file
                        # print(exact_path)
                        employees.append(exact_path)

        return employees

    def createEmbeddings(self, faceDetectorBackend):
        """Creates embeddings using the Backend Detector
        Args:
            The Face Detector Backend, and Model

        Returns:
            keyPress: Key press from the cv2 window 

        """
        embeddings = []
        # Should I by calling from faceDetect.py
        model = DeepFace.build_model(self.model)
        input_shape = (224, 224)
        input_shape = functions.find_input_shape(model)
        input_shape_x = input_shape[0]
        input_shape_y = input_shape[1]
        # From test.py line 40, used to define our model using the various model- Names

        employees = self.createEmployees(self.db_path)

        pbar = tqdm(range(0, len(employees)), desc='Finding embeddings')

        text_color = (255, 255, 255)
        # for employee in employees:
        for index in pbar:
            employee = employees[index]
            pbar.set_description("Finding embedding for %s" %
                                 (employee.split("/")[-1]))
            embedding = []

            # preprocess_face returns single face. this is expected for source images in db.
            img = functions.preprocess_face(img=employee, target_size=(
                input_shape_y, input_shape_x), enforce_detection=False, detector_backend=faceDetectorBackend)
            img_representation = model.predict(img)[0, :]

            embedding.append(employee)
            embedding.append(img_representation)
            embeddings.append(embedding)

        f = open("./db/embeddings_%s.pkl" % self.model, "wb")
        pickle.dump(embeddings, f)
        # df = pd.DataFrame(embeddings, columns = ['employee', 'embedding'])

        return embeddings


        # function updateDatabase to clear pickle file and create new one
    def deletePKL(self,faceDetectorBackend):
        """Deletes Exisiting PKL Files
        Args:
            faceDetectorBackend; Detector Backend

        """
        model = DeepFace.build_model(self.model)
        if os.path.isfile("./db/embeddings_%s.pkl" % self.model, "wb"): # check if file exists
            os.remove("./db/embeddings_%s.pkl" % self.model, "wb")

        

    def refreshPKL(self,faceDetectorBackend):
        """Deletes Exisiting PKL Files and re uploads pkl file
        Args:
            faceDetectorBackend: Detector Backend

        Returns:
            embeddings with refreshed model

        """
        self.deletePKL(faceDetectorBackend)
        embeddings = self.createEmbeddings(faceDetectorBackend)

        return embeddings



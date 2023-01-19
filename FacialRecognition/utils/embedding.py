from deepface import DeepFace
from deepface.commons import functions, distance as dst
from tqdm import tqdm

import os
import pickle

class EmbeddingGen:

    def __init__(self, db_path):
        self.db_path = db_path

    def createEmployees(self):
        employees = []
        if os.path.isdir(self.db_path) == True:
            for r, d, f in os.walk(self.db_path):  # r=root, d=directories, f = files
                for file in f:
                    if ('.jpg' in file):
                        # exact_path = os.path.join(r, file)
                        exact_path = r + "/" + file
                        # print(exact_path)
                        employees.append(exact_path)

        return employees

    def generateEmbeddings(self, modelName, faceDetectorBackend):
        embeddings = []

        employees = self.createEmployees("./db")

        if len(employees) > 0:
            model = DeepFace.build_model(modelName)
            input_shape = functions.find_input_shape(model)
            input_shape_x = input_shape[0]
            input_shape_y = input_shape[1]

            # tuned thresholds for model and metric pair
            threshold = dst.findThreshold(modelName, 'cosine')

            pbar = tqdm(range(0, len(employees)), desc='Finding embeddings')

            # TODO: why don't you store those embeddings in a pickle file similar to find function?

            if os.path.exists("./db/embeddings_VGG_Face.pkl"):
                f = open("./db/embeddings_VGG_Face.pkl", "rb")
                embeddings = pickle.load(f)
            else:

                embeddings = []
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

                
                f = open("./db/embeddings_VGG_Face.pkl", "wb")
                pickle.dump(embeddings, f)
            df = pd.DataFrame(embeddings, columns = ['employee', 'embedding'])
            df['distance_metric'] = 'cosine'



        return embeddings
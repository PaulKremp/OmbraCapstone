from deepface import DeepFace
from deepface.commons import functions, distance as dst
from deepface.detectors import FaceDetector
from tqdm import tqdm

import cv2
import os
import pandas as pd
import pickle
import time

# print(DeepFace.find("./db/user/database/Mark/IMG_20200324_153500_517.jpg", db_path="./db", enforce_detection=False, model_name="DeepFace"))


def createEmployees(db_path):
    
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


def main():
    detector_backend = "opencv"
    faceDetector = FaceDetector.build_model(detector_backend)
    input_shape = (224, 224)
    input_shape_x = input_shape[0]
    input_shape_y = input_shape[1]

    text_color = (255, 255, 255)

    employees = createEmployees("./db")

    if len(employees) > 0:
        model_name = "VGG-Face"
        model = DeepFace.build_model(model_name)
        input_shape = functions.find_input_shape(model)
        input_shape_x = input_shape[0]
        input_shape_y = input_shape[1]

        # tuned thresholds for model and metric pair
        threshold = dst.findThreshold(model_name, 'cosine')

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
                    input_shape_y, input_shape_x), enforce_detection=False, detector_backend=detector_backend)
                img_representation = model.predict(img)[0, :]

                embedding.append(employee)
                embedding.append(img_representation)
                embeddings.append(embedding)

            
            f = open("./db/embeddings_VGG_Face.pkl", "ab")
            pickle.dump(embeddings, f)
        df = pd.DataFrame(embeddings, columns = ['employee', 'embedding'])
        df['distance_metric'] = 'cosine'

        cap = cv2.VideoCapture(0)
        while True:
            start_time = time.time()
            ret, img = cap.read()
            if not ret:
                print("Could not read the image")
                exit(0)
            raw_img = img.copy()
            outputImg = img.copy()
            resolution_x = img.shape[1]
            resolution_y = img.shape[0]
            try:
                faces = FaceDetector.detect_faces(
                    faceDetector, detector_backend, img)
            except:
                faces = []
            if not faces:
                continue
            detected_faces = []
            for face, (x, y, w, h) in faces:
                detected_faces.append((x, y, w, h))
            for detected_face in detected_faces:
                x = detected_face[0]
                y = detected_face[1]
                w = detected_face[2]
                h = detected_face[3]
                custom_face = raw_img.copy()[y:y+h, x:x+w]
                custom_face = functions.preprocess_face(img=custom_face, target_size=(
                    input_shape_y, input_shape_x), enforce_detection=False, detector_backend='opencv')

                if custom_face.shape[1:3] == input_shape:
                    if df.shape[0] > 0:  # if there are images to verify, apply face recognition
                        img1_representation = model.predict(custom_face)[0, :]

                        def findDistance(row):
                            distance_metric = row['distance_metric']
                            img2_representation = row['embedding']

                            distance = 1000  # initialize very large value
                            if distance_metric == 'cosine':
                                distance = dst.findCosineDistance(
                                    img1_representation, img2_representation)
                            elif distance_metric == 'euclidean':
                                distance = dst.findEuclideanDistance(
                                    img1_representation, img2_representation)
                            elif distance_metric == 'euclidean_l2':
                                distance = dst.findEuclideanDistance(dst.l2_normalize(
                                    img1_representation), dst.l2_normalize(img2_representation))

                            return distance

                        df['distance'] = df.apply(findDistance, axis=1)
                        df = df.sort_values(by=["distance"])

                        candidate = df.iloc[0]
                        employee_name = candidate['employee']
                        best_distance = candidate['distance']

                        # print(f"Name: {employee_name}, Distance: {best_distance}")
                        #if best_distance < .2:
                            
                        cv2.rectangle(outputImg, (x, y), (x + w, y + h), (255, 0, 0), 5)
                        pass
                cv2.imshow("Image", outputImg)
                press = cv2.waitKey(5)
                if press == ord('q'):
                    cv2.destroyAllWindows()
                    exit(0)
            # print(f"FPS: {1/(time.time() - start_time)}")
    else:
        print("No employees found")
        exit(0)


if __name__ == "__main__":
    main()

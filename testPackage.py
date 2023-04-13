from sklearn.datasets import fetch_lfw_pairs
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
from deepface import DeepFace
from tqdm import tqdm
import pandas as pd


fetch = fetch_lfw_pairs(subset = 'test', color = True, resize = 1)
pairs = fetch.pairs
labels = fetch.target
target_names = fetch.target_names

actuals = []
predictions = []

instances = pairs.shape[0]
pbar = tqdm(range(0, instances))

for i in pbar:
    pair = pairs[i]
    img1 = pairs[0]
    img2 = pairs[1]

    # fig = plt.figure()

    # ax1 = fig.add_subplot(1,3,1)
    # plt.imshow(img1/255)

    # ax2 = fig.add_subplot(1,3,2)
    # plt.imshow(img2/255)

    # ax3 = fig.add_subplot(1,3,3)
    # plt.text(0,0.5,target_names[labels[i]])

    # plt.show()

    img1 = img1[:,:,::-1]
    img2 = img2[:,:,::-1]
    obj = DeepFace.verify(img1, img2, model_name = 'Dlib', distance_metric = 'euclidean')
    prediction = obj["verified"]
    predictions.append(prediction)
    actual = True if labels[i] == 1 else False
    actuals.append(actual)

    accuracy = 100*accuracy_score(actuals, predictions)
    precision = 100*precision_score(actuals, predictions)
    recall = 100*recall_score(actuals, predictions)
    f1 = 100*f1_score(actuals, predictions)

    print(accuracy)
    print(precision)
    print(recall)
    print(f1)
    cm = confusion_matrix(actuals, predictions)
    print(cm)

    tn, fp, fn, tp = cm.ravel()
    print(tn, fp, fn, tp)
'''
how to use
python main.py 995942 Mang.Jajang Jajang
995942 is NIK
Mang.Jajang is name
Jajang is nickname
'''


import cv2
from align_custom import AlignCustom
from face_feature import FaceFeature
from mtcnn_detect import MTCNNDetect
from tf_graph import FaceRecGraph
from auto_bright import automatic_brightness_and_contrast
from vector_image import vector_image
import argparse
import sys
import json
import time
import datetime
import numpy as np
import os


def main():
    # nik = sys.argv[2]
    #ktp = sys.argv[14]
    name = sys.argv[1]
    # nickname = sys.argv[3]

    # print(nik)
    # print(name)
    # print(nickname)

    new_name = str(name)
    mirror(new_name)


def mirror(new_name):
    while True:
        _, frame = vs.read()
        cv2.imshow(".:: SIAPKAN POSISI ANDA DENGAN TEGAP LURUS::.", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            cv2.destroyAllWindows()
            break
    create_manual_data(new_name)


def create_manual_data(new_name):

    a = 1
    f = open(path_model_training + 'newmodel.txt', 'r')
    data_set = json.loads(f.read())
    person_imgs = []
    person_features = []
    print("Please start turning slowly. Press 'q' to save and add this new user to the dataset")

    while True:
        _, frame = vs.read()
        rects, landmarks = face_detect.detect_face(
            frame, 80)  # min face size is set to 80x80
        for (i, rect) in enumerate(rects):
            aligned_frame, pos = aligner.align(160, frame, landmarks[:, i])
            auto_result, alpha, beta = automatic_brightness_and_contrast(aligned_frame)
            cartoon, color, edges, img = vector_image(auto_result)
            if len(aligned_frame) == 160 and len(aligned_frame[0]) == 160:
                b = str(a)
                a += 1
                person_imgs.append(cartoon)
                cv2.rectangle(frame, (rect[0], rect[1]),
                              (rect[2], rect[3]), (255, 0, 0))
                cv2.putText(frame, " ambil foto ke-"+b, (350, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.imshow("Captured face", cartoon)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q") or a == 100:
            break
    person_features = [
        np.mean(extract_feature.get_features(person_imgs), axis=0).tolist()]
    data_set[new_name] = person_features
    print("has been trained")

    f = open(path_model_training + 'newmodel.txt', 'w')
    f.write(json.dumps(data_set))
    # print(data_set)
    # print(person_features)


if __name__ == '__main__':

    # Video Input
    vs = cv2.VideoCapture(0)

    # DIR PATH DEFINE
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    path_models = os.path.join(ROOT_DIR, 'models/')
    path_model_training = os.path.join(ROOT_DIR, 'model_training/')

    # Module Facenet, GRAPH, FEATURE
    FRGraph = FaceRecGraph()
    MTCNNGraph = FaceRecGraph()
    aligner = AlignCustom()
    extract_feature = FaceFeature(FRGraph)
    # scale_factor, rescales image for faster detection
    face_detect = MTCNNDetect(MTCNNGraph, scale_factor=2)
    main()
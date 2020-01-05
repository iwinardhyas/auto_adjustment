from align_custom import AlignCustom
from face_feature import FaceFeature
from mtcnn_detect import MTCNNDetect
from tf_graph import FaceRecGraph
from collections import deque
import matplotlib.pyplot as plt
import cv2
import numpy as np
import sys
import json
import time
import datetime
import os

f = open('/home/erwin/Documents/FaceRec-master_iwin/model_training/employeeguest.json','r')
data_set = json.loads(f.read())
FRGraph = FaceRecGraph()
MTCNNGraph = FaceRecGraph()
aligner = AlignCustom()
extract_feature = FaceFeature(FRGraph)
face_detect = MTCNNDetect(MTCNNGraph, scale_factor=2)

def findPeople(features_arr, thres = 0.6, percent_thres = 85):
    returnRes = []
    result = "Unregistered"
    smallest = sys.maxsize
    for person in data_set.keys():
        person_data = data_set[person]['person_feature']
        distance = np.sqrt(np.sum(np.square(person_data-features_arr)))
        print('ini distance= ',distance)
        if(distance < smallest):
            smallest = distance
            result = data_set[person]['nik']
    percentage =  min(100, 100 * thres / smallest)
    print('ini smallest= ',smallest)
    print('ini percent= ',percentage)
    print('NIK: ',result)
    if percentage <= percent_thres:
        result = "Unregistered"
    returnRes.append(result)
    return returnRes

benar = 0
salah = 0
counter = 1
rootdir = "/home/erwin/Desktop/photo_register/23434"
# for files in os.listdir(rootdir):
#     new_name = rootdir+'/'+files
#     print(new_name)
    # for file in files:
    #     if file.endswith(".jpg"):
    #         # try:
    #         vs = os.path.join(subdir, file)
    #         # print(vs)
frame = cv2.imread('/home/erwin/Desktop/1_670074_DST0163_08:59:27.176995.jpg')
    # rects, landmarks = face_detect.detect_face(frame,20)
    # for (i, rect) in enumerate(rects):
    #     cv2.rectangle(frame,(rect[0],rect[1]),(rect[2],rect[3]),(0,255,0),2)
    #     aligned_face, face_pos = aligner.align(160,frame,landmarks[:,i])
    # # aligned_face, face_pos = aligner.align(160,frame,landmarks[:,i])
    # # frame = plt.imread(vs, format=None)
    # # frame = vs.read()
    # # frame = frame[:, :, (2, 0, 1)]
    # # print(frame)
    # # print(type(frame))
    # # cv2.imshow(frame)
# global features_arr
features_arr = extract_feature.get_features(frame)
recog_data = findPeople(features_arr)
    # print(recog_data)
    #     if new_name==recog_data[0]:
    #         benar = benar + 1
    #     else:
    #         salah = salah + 1
    # except:
    #     continue
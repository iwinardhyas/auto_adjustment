import sys
import cv2
import json
sys.path.insert(0, '../imagezmq')  # imagezmq.py is in ../imagezmq
import imagezmq
import numpy as np
from vector_image import vector_image
from matplotlib import pyplot as plt
from auto_bright import automatic_brightness_and_contrast
from align_custom import AlignCustom
from face_feature import FaceFeature
from mtcnn_detect import MTCNNDetect
from tf_graph import FaceRecGraph
from auto_bright import automatic_brightness_and_contrast
from vector_image import vector_image

image_hub = imagezmq.ImageHub()
f = open('/home/erwin/Documents/FaceRec-master_iwin/model_training/newmodel.txt', 'r')
data_set = json.loads(f.read())
FRGraph = FaceRecGraph()
# MTCNNGraph = FaceRecGraph()
# aligner = AlignCustom()
extract_feature = FaceFeature(FRGraph)

def findPeople(features_arr, thres = 0.6, percent_thres = 80):
    returnRes = []
    for (i,features_512D) in enumerate(features_arr):
        result = "Unregistered"
        smallest = sys.maxsize
        for person in data_set.keys():
            person_data = data_set[person]
            distance = np.sqrt(np.sum(np.square(person_data-features_512D)))
            if(distance < smallest):
                smallest = distance
                result = person
        percentage =  min(100, 100 * thres / smallest)
        if percentage <= percent_thres :
            result = "Unregistered"
        returnRes.append((result,percentage))
    return returnRes


while True:  # press Ctrl-C to stop image display program
    image_name, image = image_hub.recv_image()
    # auto_result, alpha, beta = automatic_brightness_and_contrast(image)
    # cartoon, color, edges, img = vector_image(auto_result)
    # features_arr = extract_feature.get_features(image)
    # findPeople(features_arr)
    # print(features_arr)

    cv2.imshow(image_name, image)
    features_arr = extract_feature.get_features(image)

    # cv2.waitKey(1)  # wait until a key is pressed
    # image_hub.send_reply(b'OK')
    # key = cv2.waitKey(1) & 0xFF
    # if key == ord("q"):
    #     break
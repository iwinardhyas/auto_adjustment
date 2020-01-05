import zmq
import numpy as np
import cv2
import sys
import cv2
import json
from align_custom import AlignCustom
from face_feature import FaceFeature
from mtcnn_detect import MTCNNDetect
from tf_graph import FaceRecGraph

# f = open('/home/erwin/Documents/FaceRec-master_iwin/model_training/newmodel.txt', 'r')
# data_set = json.loads(f.read())
# FRGraph = FaceRecGraph()

# MTCNNGraph = FaceRecGraph()
# aligner = AlignCustom()

# extract_feature = FaceFeature(FRGraph)

context = zmq.Context()
# receiver = context.socket(zmq.PULL)
receiver = context.socket(zmq.SUB)
receiver.connect("tcp://localhost:5555")

# sender = context.socket(zmq.PUSH)
# sender.connect("tcp://localhost:5556")

while True:
    image = receiver.recv_pyobj()
    cv2.imshow('tes',image)
    cv2.waitKey(1)
    # features_arr = extract_feature.get_features(image)
    # print(features_arr)
    # fft = np.fft.fft2(image)
    # print(fft)
    # cv2.destroyAllWindows()
    # sender.send_pyobj(fft)
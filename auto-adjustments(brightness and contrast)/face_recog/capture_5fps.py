from mtcnn_detect import MTCNNDetect
from tf_graph import FaceRecGraph
from align_custom import AlignCustom
from face_feature import FaceFeature
# sys.path.insert(0, '../imagezmq')  # imagezmq.py is in ../imagezmq
import imagezmq
import cv2
import os
import math
import time
import zmq

FRGraph = FaceRecGraph()
MTCNNGraph = FaceRecGraph()
face_detect = MTCNNDetect(MTCNNGraph, scale_factor=2)
aligner = AlignCustom()
sender = imagezmq.ImageSender()
FRGraph = FaceRecGraph()
extract_feature = FaceFeature(FRGraph)

context = zmq.Context()

listgambar = [1,2,3,4,5,6,7,8,9,10]
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

def camera_recog():
    print("[INFO] camera sensor warming up...")
    vs = cv2.VideoCapture(2)
    vs.set(cv2.CAP_PROP_FPS,3)
    waktu_awal = time.time()
    counter = 0
    while True:
        _,frame = vs.read()
        detect_time = time.time()
        rects, landmarks = face_detect.detect_face(frame,120) #min face size is set to 80x80
        aligns = []
        positions = []
        counter += 1
        for (i, rect) in enumerate(rects):
            if i==0:
                cv2.rectangle(frame,(rect[0],rect[1]),(rect[2],rect[3]),(0,255,0),2)
                aligned_face, face_pos = aligner.align(160,frame,landmarks[:,i])
                # features_arr = extract_feature.get_features(aligned_face)
                # print(features_arr)
                # getvalue = vs.get(1)
                # if (getValue % math.floor(frameRate) == 0):
                sender.send_image('tes', aligned_face)
                # message = socket.recv()
                # if len(aligned_face) == 160 and len(aligned_face[0]) == 160:
                #     aligns.append(aligned_face)
                #     positions.append(face_pos)
            else:
                continue
        
        cv2.imshow('tes',frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            waktu_akhir = time.time()
            print('fps: '+str(counter/(waktu_akhir-waktu_awal)))
            break
    vs.release()
camera_recog()
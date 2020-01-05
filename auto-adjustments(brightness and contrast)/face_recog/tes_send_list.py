from align_custom import AlignCustom
from face_feature import FaceFeature
from mtcnn_detect import MTCNNDetect
from tf_graph import FaceRecGraph
from collections import deque
import cv2
import numpy as np
import sys
import json
import time
import os
import datetime
import serial
import psycopg2
import requests
import screeninfo
import vlc
import zmq
import pandas as pd
import codecs

context = zmq.Context()
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

def draw_border(img, pt1, pt2, color, thickness, r, d):
    x1,y1 = pt1
    x2,y2 = pt2

    text = 'FIT YOUR FACE INTO THE AREA BELLOW'
    cv2.putText(img,text,(20,150),cv2.FONT_HERSHEY_TRIPLEX,1.5,(0,0,0),1,cv2.LINE_AA)

    # Top left
    cv2.line(img, (x1 + r, y1), (x1 + r + d, y1), color, thickness)
    cv2.line(img, (x1, y1 + r), (x1, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)

    # Top right
    cv2.line(img, (x2 - r, y1), (x2 - r - d, y1), color, thickness)
    cv2.line(img, (x2, y1 + r), (x2, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)

    # Bottom left
    cv2.line(img, (x1 + r, y2), (x1 + r + d, y2), color, thickness)
    cv2.line(img, (x1, y2 - r), (x1, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)

    # Bottom right
    cv2.line(img, (x2 - r, y2), (x2 - r - d, y2), color, thickness)
    cv2.line(img, (x2, y2 - r), (x2, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)

    overlay = img.copy()

    alpha = 0.7
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

# [30:480 , 218:425]

def camera_recog():
    print("[INFO] camera sensor warming up...")
    vs = cv2.VideoCapture(2)

    # vs.set(cv2.CAP_PROP_FPS,3)
    while True:
        _,frame = vs.read()
        contrast = 100
        brightness = -50
        frame = np.int16(frame)
        frame = frame * (contrast/127+1) - contrast + brightness
        frame = np.clip(frame, 0, 255)
        frame = np.uint8(frame)
        detect_time = time.time()
        rects, landmarks = face_detect.detect_face(frame,100);#min face size is set to 80x80
        aligns = []
        positions = []
        recog_data = " "

        for (i, rect) in enumerate(rects):
            if i==0:
                cv2.rectangle(frame,(rect[0],rect[1]),(rect[2],rect[3]),(0,255,0),2)
                aligned_face, face_pos = aligner.align(160,frame,landmarks[:,i])
                if len(aligned_face) == 160 and len(aligned_face[0]) == 160:
                    aligns.append(aligned_face)
                    positions.append(face_pos)
            else:
                continue

        if(len(aligns) > 0):
            features_arr = extract_feature.get_features(aligns)
            # socket.send_json(features_arr.tolist())
            # message = socket.recv()
            # print(features_arr)
            
        # cv2.namedWindow('projector', cv2.WND_PROP_FULLSCREEN)
        # cv2.moveWindow('projector', screen.x - 1, screen.y - 1)
        # cv2.setWindowProperty('projector', cv2.WND_PROP_FULLSCREEN,
        #                       cv2.WINDOW_FULLSCREEN)
        cv2.imshow('projector', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    vs.release()

def findPeople(features_arr, positions, thres = 0.6, percent_thres = 88):
    
    returnRes = []
    for (i,features_128D) in enumerate(features_arr):
        result = "Unregistered"
        smallest = sys.maxsize
        for person in data_set.keys():
            person_data = data_set[person]['person_feature']
            distance = np.sqrt(np.sum(np.square(person_data-features_128D)))
            if(distance < smallest):
                smallest = distance
                result = person
        percentage =  min(100, 100 * thres / smallest)
        if percentage <= percent_thres :
            result = "Unregistered"
        returnRes.append((result,percentage))
    print(percentage)
    return returnRes

tempvar = deque(['a','b'])
savename = deque()
savetime = deque()
FRGraph = FaceRecGraph()
MTCNNGraph = FaceRecGraph()
aligner = AlignCustom()
extract_feature = FaceFeature(FRGraph)
face_detect = MTCNNDetect(MTCNNGraph, scale_factor=2) #scale_factor, rescales image for faster detection
screen_id = 0
screen = screeninfo.get_monitors()[screen_id]


camera_recog()

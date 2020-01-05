import time
import zmq
import cv2
import json
import os
import re
import sys
import numpy as np

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
# global tempvar
f = open('/home/erwin/Documents/FaceRec-master/model_training/employeeguest.json', 'r')
data_set = json.loads(f.read())

def findPeople(features_arr, thres = 0.6, percent_thres = 88):
    
    returnRes = []
    for (i,features_128D) in enumerate(features_arr):
        result = "Unregistered"
        smallest = sys.maxsize
        for person in data_set.keys():
            person_data = data_set[person]['person_feature']
            # print(person_data)
            # import ipdb; ipdb.set_trace()
            person_data = np.array(person_data[0])
            features_128D = np.array(features_128D)
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

while True:
    recog_data = " "
    #  Wait for next request from client
    message = json.loads(socket.recv())
    # print(message)
    recog_data = findPeople(message)
    # print(recog_data)
    if recog_data[0][0]!="Unregistered":
        tempvar = []
        tempvar.append(recog_data[0][0])
        if len(tempvar)==3:                         
            print(recog_data)
    #         tempvar.pop()
    #         if tempvar[0]==tempvar[1] and tempvar[0] not in savename:
    #             savename.appendleft(tempvar[0])
    #             tempvar = deque(['a','b'])

    # print("Received request: %s" % message)

    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client
    socket.send(b'recog_data')
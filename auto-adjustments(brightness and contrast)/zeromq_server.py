import time
import zmq
import cv2
import json
import os
import re

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = json.loads(socket.recv())
    message = re.sub('[/]','',message)
    # print("Received request: %s" % message)

    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client
    socket.send(b"thank you")
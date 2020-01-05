import sys
import zmq

port = "5556"

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")

print ("Collecting updates from weather server...")
socket.connect ("tcp://localhost:5555")

while True:
    print (socket.recv())
import zmq
import time
from elasticsearch import Elasticsearch
from uuid import uuid4
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--device_id", help="Device ID that must send the weather data",
                    action="store")
args = parser.parse_args()

device_id = ""
if args.device_id:
    device_id = args.device_id
    print("Device ID is set up for {device_id}!".format(device_id=device_id))

context = zmq.Context()

sock = context.socket(zmq.SUB)

sock.setsockopt(zmq.SUBSCRIBE, b"device_id")
sock.connect("tcp://127.0.0.1:5600")

es = Elasticsearch()

if device_id != "":

	while True:
		raw_message = sock.recv()
		message = json.loads(raw_message.split(" --> ")[1])

		print (raw_message)

		doc = {
			"device_id": device_id,
			"message_id": message["message_id"], 
			"humidity": message["humidity"], 
			"temperature_in_celsius": message["temperature_in_celsius"], 
			"createdAt": message["createdAt"]
		}

		res = es.index(index="myiot", doc_type='weather', id=str(uuid4()), body=doc)
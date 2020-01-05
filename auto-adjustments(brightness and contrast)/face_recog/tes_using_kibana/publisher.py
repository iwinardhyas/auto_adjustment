import zmq
import json
import random
import time
from uuid import uuid4
from datetime import datetime
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

sock = context.socket(zmq.PUB)
# sock.setsockopt(zmq.SUBSCRIBE, b"")
sock.bind("tcp://127.0.0.1:5600")

def send_message(topic, id, timestamp, payload):

	# Message [prefix][message]
	message = "{topic} #{id} at {timestamp} --> {payload}  ".format(topic=topic, id=id, timestamp=timestamp, payload=payload)
	sock.send(b"message")

if device_id != "":
	while True:
		message_id, now = str(uuid4()), datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		humidity = random.randrange(20, 40)
		temperature_in_celsius = random.randrange(32, 41)

		payload = json.dumps({"message_id": message_id, "humidity":humidity, "temperature_in_celsius":temperature_in_celsius, "createdAt":now})
		send_message(device_id, message_id, now, payload)

		time.sleep(1)
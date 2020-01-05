from time import sleep
import zmq
import cv2
from mtcnn_detect import MTCNNDetect
from tf_graph import FaceRecGraph
from align_custom import AlignCustom
from face_feature import FaceFeature

FRGraph = FaceRecGraph()
MTCNNGraph = FaceRecGraph()
face_detect = MTCNNDetect(MTCNNGraph, scale_factor=2)
aligner = AlignCustom()
FRGraph = FaceRecGraph()
extract_feature = FaceFeature(FRGraph)

context = zmq.Context()
# socket = context.socket(zmq.PUSH)
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")
cap = cv2.VideoCapture(0)
# sleep(2)

# for i in range(100):
#     ret, frame = cap.read()
#     # cv2.imshow('tessss',frame)
#     # cv2.waitKey(0)
#     socket.send_pyobj(frame)
#     print('Sent frame {}'.format(i))
while True:
    ret, frame = cap.read()
    # detect_time = time.time()
    rects, landmarks = face_detect.detect_face(frame,120) #min face size is set to 80x80
    aligns = []
    positions = []
    # counter += 1
    for (i, rect) in enumerate(rects):
        if i==0:
            cv2.rectangle(frame,(rect[0],rect[1]),(rect[2],rect[3]),(0,255,0),2)
            aligned_face, face_pos = aligner.align(160,frame,landmarks[:,i])
            socket.send_pyobj(aligned_face)
            print('sent frame {}',i)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        # waktu_akhir = time.time()
        # print('fps: '+str(counter/(waktu_akhir-waktu_awal)))
        break
vs.release()
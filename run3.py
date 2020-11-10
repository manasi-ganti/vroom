#python3 run.py --prototxt deploy.prototxt.txt --model res10_300x300_ssd_iter_140000.caffemodel --shape-predictor shape_predictor_68_face_landmarks.data
# import the necessary packages
from imutils import face_utils
import imutils
#from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils.video import FileVideoStream
import numpy as np
import argparse
import dlib
import time
import cv2
import math
import detect as det
import csv
from datetime import date
from datetime import datetime
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
#import pandas as pd
#import pandas_datareader as pdr

#import webcam as wc

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
	help="path to Caffe pre-trained model")
#ap.add_argument("-c", "--confidence", type=float, default=0.5,
#	help="minimum probability to filter weak detections")
ap.add_argument("-s", "--shape-predictor", required=True,
	help="path  to facial landmark predictor")

ap.add_argument("-v", "--smiling-video", required=True,
	help = "path to video of smiling")
args = vars(ap.parse_args())

# define two constants, one for the eye aspect ratio to indicate
# blink and then a second constant for the number of consecutive
# frames the eye must be below the threshold
EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 3
# initialize the frame counters and the total number of blinks
COUNTER = 0
TOTAL = 0

#create facial landma rk predictor
predictor = dlib.shape_predictor(args["shape_predictor"])
# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])
# initialize the video stream and allow the camera sensor to warm up
#print("[INFO] starting video stream...")
#vs = FileVideoStream(path=args["smiling_video"]).start() #"/Users/manasi/Documents/data/smiling1.mp4").start()
#fileStream = True
#vs = VideoStream(src = 0).start()
#fileStream = False
time.sleep(2.0)

faces = []
landmarks = []

def calibrate():
	print("[INFO] starting file video stream...")
	vs = FileVideoStream(path=args["smiling_video"]).start() #"/Users/manasi/Documents/data/smiling1.mp4").start()
	fileStream = True
	#vs = VideoStream(src = 0).start()
	#fileStream = False
	time.sleep(2.0)
	mouths = []
	while True:
		if not vs.more():
			break
		frame = vs.read()
		if frame is None:
			break
		frame = imutils.resize(frame, width = 400)
		# get frame dimensions and convert it to a blob
		(h, w) = frame.shape[:2]
		blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

		# pass the blob through the network and obtain the detections and predictions
		net.setInput(blob)
		detections = net.forward()
		initial_ar = 0
		# loop over the detections
		for i in range(0, detections.shape[2]):
			# filter out weak detections by ensuring the confidence > minimum confidence
			confidence = detections[0, 0, i, 2]
			if confidence < .5:
				continue

			# compute the coordinates of the bounding box for the object
			box = detections[0, 0, i, 3:7]*np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")
			faces.append((startX, startY, endX, endY))

			shape = predictor(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), dlib.rectangle(startX, startY, endX, endY))
			shape = face_utils.shape_to_np(shape)
			landmarks.append(shape)

			text = "{:.2f}%".format(confidence*100)
			if(startY - 10 > 10):
				y = startY - 10 
			else:
				startY + 10
			cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2) #face
			for (x, y) in shape:
				cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
				cv2.putText(frame, text, (startX, startY), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2) # face confidence
		cv2.imshow("Frame", frame)
		#print(n)
		key = cv2.waitKey(1) & 0xFF

		# if the 'q' key is pressed, break
		if key == ord("q"):
			break
	# cleanup
	cv2.destroyAllWindows() 
	vs.stop()

def w_thres(first, second):
	threshold = ((landmarks[0][first][0]-landmarks[0][second][1])/(faces[0][2]-faces[0][0]))
	print("threshold")
	print(threshold)
	return threshold

def writeAnalytics(file_name, rows, names, values, engagement):
	with open(date.today().strftime("%m-%d-%y") + '.csv', 'w', newline='') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',',quotechar='\'', quoting=csv.QUOTE_MINIMAL)
		for num in range(0, rows):
			spamwriter.writerow([names[num],values[num]])

def webcam():
	print("[INFO] starting video stream...")
	vs = VideoStream(src = 0).start()
	time.sleep(2.0)
	if os.path.exists(report_file_name):
		os.remove(report_file_name)
	else:
		print("hi.csv does not exist")
	n = -1 #frame counting
	m = 0 #smile counting
	w = 0 #wide eyed counting
	s = 0 #squint counting
	close = 0 #close up counting
	far = 0 #far away counting
	frame1 = 0 #initial frame
	variables = [] #for reporting
	values = []
	# loop over the frames from the video stream
	while True:
		n+=1;
		engagement.append(0)
		real_frame = vs.read()
		if real_frame is None:
			break
		real_frame = imutils.resize(real_frame, width = 400)

		#frame = np.zeros((500, 640, 3),np.uint8)
		frame = np.array(Image.open('defaultphoto.jpg'))
		frame = imutils.resize(frame, width = 400)

		if n==0:
			frame1 = real_frame
		#vs = VideoStream(src = 0).start()
		isSmile = det.Detect(net, predictor).smile(real_frame, .4)
 		# if the 'q' key is pressed, break
		if isSmile: #key == ord("p")
			#print("HI")
			frame = cv2.imread("smilingpic.png")
			frame = imutils.resize(frame, width = 400)
			m+= 1
			engagement[n] += 1

		isWide = det.Detect(net, predictor).wide(real_frame)
		if isWide:
			#print("WIDE")
			w+=1
			engagement[n] += 1

		isSquint = det.Detect(net, predictor).squint(real_frame)
		if isSquint:
			#print("SQUINT")
			#frame = cv2.imread("smilingpic.png")
			s+=1
			engagement[n] -= 1

		size_diff = det.Detect(net, predictor).size_difference(real_frame, frame1)
		print(size_diff)
		if size_diff > 1.5:
			close += 1
			engagement[n] += 1

		elif size_diff < .75:
			far += 1
			engagement[n] -= 1

		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break

		print(engagement)
	variables = ["SMILE %", "WiDe %","sQuInt %", "close %", "FAR %"]
	if n != 0:
		values = [(m/n)*100, (w/n)*100, (s/n)*10, (close/n)*100, (far/n)*100]
	writeAnalytics(report_file_name, 5, variables, values, engagement)

	# cleanup
	cv2.destroyAllWindows()
	vs.stop()


#calibrate()
report_file_name = date.today().strftime("%m-%d-%y") + '.csv'
engagement = [0] #over all frames
webcam()
with open(report_file_name, newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	for row in spamreader:
		print(', '.join(row))

indexes = [0]*len(engagement)
for i in range(0, len(indexes)):
	indexes[i] = i
print(len(indexes))
print(len(engagement))
plt.scatter(indexes, engagement)
plt.show()

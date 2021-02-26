import argparse
import csv
import cv2
from datetime import date
from datetime import datetime
from . import detect as det
from . import src_path
import dlib
import http.client
import imutils
from imutils import face_utils
from imutils.video import FileVideoStream
from imutils.video import VideoStream
import math
import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
import time
import requests
import json

def vroom(args):

	vr = Vroom(args)
	vr.webcam([src_path+"/defaultpic.png",src_path+"/smilepic.png",src_path+"/squintpic.png",src_path+"/widepic.png"])

class Vroom:

	#create facial landmark predictor
	predictor = dlib.shape_predictor(src_path + "/shape_predictor_68_face_landmarks.dat") #/Users/manasi/Documents/zoom2/shape_predictor_68_face_landmarks.dat")
	# load our serialized model from disk
	print("[INFO] loading model...")
	net = cv2.dnn.readNetFromCaffe(src_path + "/deploy.prototxt.txt", src_path + "/res10_300x300_ssd_iter_140000.caffemodel")
	time.sleep(2.0)
	report_file_name = date.today().strftime("%m-%d-%y")


	def __init__(self, args):
		self.faces = []
		self.landmarks = []
		self.engagement = [0] #over all frames
		self.args = args
		self.zoom_session = requests.Session()
		self.zoom_req_headers = { 'authorization': ("Bearer " + args["token"])}
		self.current_profile_pic = 'defaultpic.png'

	def calibrate(self, video_path):
		print("[INFO] starting file video stream...")
		vs = FileVideoStream(path=video_path).start() 
		fileStream = True
		time.sleep(2.0)
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
			Vroom.net.setInput(blob)
			detections = Vroom.net.forward()
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
				self.faces.append((startX, startY, endX, endY))

				shape = Vroom.predictor(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), dlib.rectangle(startX, startY, endX, endY))
				shape = face_utils.shape_to_np(shape)
				self.landmarks.append(shape)

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
			key = cv2.waitKey(1) & 0xFF

			# if the 'q' key is pressed, break
			if key == ord("q"):
				break
		# cleanup
		cv2.destroyAllWindows() 
		vs.stop()

	def w_thres(self, first, second):
		threshold = ((self.landmarks[0][first][0]-self.landmarks[0][second][1])/(self.faces[0][2]-self.faces[0][0]))
		print("threshold")
		print(threshold)
		return threshold

	def writeAnalytics(file_name, rows, names, values, engagement):
		if os.path.exists(file_name):#Vroom.report_file_name + '.csv'):
			os.remove(file_name)#Vroom.report_file_name+'.csv')
		with open(file_name, 'w', newline='') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=',',quotechar='\'', quoting=csv.QUOTE_MINIMAL)
			for num in range(0, rows):
				spamwriter.writerow([names[num],values[num]])


	def changePFP(self, filename):
		userid = self.args["userid"]
		jwt_token = self.args["token"] 
		filepath = src_path + '/' + filename 

		url = 'https://api.zoom.us/v2/users/{0}/picture'.format(userid)

		headers = {'Authorization': 'Bearer {}'.format(jwt_token),
		           'Accept': 'application/json',
		           }
		files = {'pic_file': open(filepath, 'rb')}

		response = requests.post(url, files=files, headers=headers)

	def isMeetingOver(self):
		res = self.zoom_session.get("https://api.zoom.us/v2/meetings/" + self.args["meetingid"], headers=self.zoom_req_headers)
		obj = res.json()
		try:
			status = (obj["status"])
		except KeyError as e:
			print(obj)
			return True
		if(status == "waiting"):
			return True
		return False


	def webcam(self, pictures):
		print("[INFO] starting video stream...")
		vs = VideoStream(srcs = 0).start()
		time.sleep(2.0)
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
		net = Vroom.net
		predictor = Vroom.predictor
		while True:
			n+=1;
			self.engagement.append(0)

			real_frame = vs.read()
			if real_frame is None:
				break
			real_frame = imutils.resize(real_frame, width = 400)
			if n==0:
				frame1 = real_frame
			if type(real_frame) == None:
				continue
			isWide = det.Detect(Vroom.net, Vroom.predictor).wide(real_frame)
			isSquint = det.Detect(Vroom.net, Vroom.predictor).squint(real_frame)
			isSmile = det.Detect(Vroom.net, Vroom.predictor).smile(real_frame, .4)
			
			file_name = ("defaultpic.png")

			if isWide:
				w+=1
				self.engagement[n] += 1
				file_name = ("widepic.png")
			if isSquint:
				s+=1
				self.engagement[n] -= 1
				file_name = ("squintpic.png")
			if isSmile: 
				m+= 1
				self.engagement[n] += 1
				file_name = ("smilepic.png")

			size_diff = det.Detect(Vroom.net, Vroom.predictor).size_difference(real_frame, frame1)
			#CLOSE
			if size_diff > 1.5:
				close += 1
				self.engagement[n] += 1
			#FAR
			elif size_diff < .75:
				far += 1
				self.engagement[n] -= 1

			#show
			if(file_name != self.current_profile_pic):
				self.changePFP(file_name)
				self.current_profile_pic = file_name
			if(n%2000):
				variables = ["percentage of time smiling", "percentage of time wide-eyed","percentage of time squinting", "percentage of time close to camera", "percentage of time far from camera"]
				if n != 0:
					values = [(m/n)*100, (w/n)*100, (s/n)*100, (close/n)*100, (far/n)*100]
				else:
					values = [0,0,0,0,0]
				Vroom.writeAnalytics(Vroom.report_file_name + '.csv', len(variables), variables, values, self.engagement)

				with open(Vroom.report_file_name + '.csv', newline='') as csvfile:
					spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
					for row in spamreader:
						print(', '.join(row))
				indexes = [0]*len(self.engagement)

				for i in range(0, len(indexes)):
					indexes[i] = i
				plt.clf()
				plt.scatter(indexes, self.engagement)

				if os.path.exists(Vroom.report_file_name +'.png'):
					os.remove(Vroom.report_file_name+'.png')
				plt.savefig(Vroom.report_file_name + ".png")#vr.report_file_name+'.png')

		# cleanup
		cv2.destroyAllWindows()
		vs.stop()


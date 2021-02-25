#python3 my_detect_faces_video.py --prototxt deploy.prototxt.txt --model res10_300x300_ssd_iter_140000.caffemodel --shape-predictor shape_predictor_68_face_landmarks.data
# import the necessary packages
from imutils import face_utils
import imutils
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils.video import FileVideoStream
import numpy as np
import argparse
import dlib
import time
import cv2
import math


class Detect:
	def __init__(self, face_detector, shape_predictor):
		self.face_detector = face_detector
		self.shape_predictor = shape_predictor
		self.counter = 0

	# define two constants, one for the eye aspect ratio to indicate
	# blink and then a second constant for the number of consecutive
	# frames the eye must be below the threshold
	EYE_AR_THRESH = 0.3
	EYE_AR_CONSEC_FRAMES = 3
	
	def eye_aspect_ratio(self, eye):
		# compute the euclidean distances between the two sets of
		# vertical eye landmarks (x, y)-coordinates
		A = dist.euclidean(eye[1], eye[5])
		B = dist.euclidean(eye[2], eye[4])

		# compute the euclidean distance between the horizontal
		# eye landmark (x, y)-coordinates
		C = dist.euclidean(eye[0], eye[3])

		# compute the eye aspect ratio
		ear = (A + B)/(2.0 * C)
		return ear


	def faces(self, frame):
		# get frame dimensions and convert it to a blob
		(h, w) = frame.shape[:2]
		blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

		# pass the blob through the network and obtain the detections and predictions
		self.face_detector.setInput(blob)
		detections = self.face_detector.forward()
		initial_ar = 0
		# loop over the detections
		for i in range(0, detections.shape[2]):
			# filter out weak detections by ensuring the confidence > minimum confidence
			confidence = detections[0, 0, i, 2]
			if confidence < .5:
				continue
			# compute the coordinates of the bounding box for the object
			box = detections[0, 0, i, 3:7]*np.array([w, h, w, h])
			return box

	def landmarks(self, frame):
		face = self.faces(frame)
		(startX, startY, endX, endY) = face.astype("int")

		shape = self.shape_predictor(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), dlib.rectangle(startX, startY, endX, endY))
		shape = face_utils.shape_to_np(shape)
		return shape
	
	def blink(self, frame):
		#face = self.faces(frame)
		shape = self.landmarks(frame)
		# blink checking
		leftEAR = self.eye_aspect_ratio(shape[36:42])
		rightEAR = self.eye_aspect_ratio(shape[42:48])
		ear = (leftEAR + rightEAR)/2.0

		# check to see if the eye aspect ratio is below the blink
		# threshold, and if so, increment the blink frame counter
		if ear < Detect.EYE_AR_THRESH:
			return True
			self.counter += 1
		# otherwise, the eye aspect ratio is not below the blink
		# threshold
		else:
			# if the eyes were closed for a sufficient number of
			# then increment the total number of blinks
			if self.counter >= Detect.EYE_AR_CONSEC_FRAMES:
				self.counter = 0
				return True
		# reset the eye frame counter
		self.counter = 0
		return False

	def wide(self, frame):
		shape = self.landmarks(frame)
		# compute eye aspect ratios
		leftEAR = self.eye_aspect_ratio(shape[36:42])
		rightEAR = self.eye_aspect_ratio(shape[42:48])
		ear = (leftEAR + rightEAR)/2.0

		# check to see if the eye aspect ratio is below the
		# threshold, and if so,return False
		if ear < Detect.EYE_AR_THRESH +.02:
			return False
		else:
			return True

	def squint(self, frame):
		shape = self.landmarks(frame)
		# compute eye aspect ratios
		leftEAR = self.eye_aspect_ratio(shape[36:42])
		rightEAR = self.eye_aspect_ratio(shape[42:48])
		ear = (leftEAR + rightEAR)/2.0

		# check to see if the eye aspect ratio is below the
		# threshold, and if so,return True
		if ear < Detect.EYE_AR_THRESH:
			return True
		else:
			return False

	def smile(self, frame, width_threshold):
		face = self.faces(frame)
		shape = self.landmarks(frame)
		(x1, y1, x2, y2) = face.astype("int")

		mouth_width = shape[54][0]-shape[48][0]
		mouth_height = shape[57][1]-shape[51][1]

		return (mouth_width)/(x2-x1)>(width_threshold - .02)

	def size_difference(self, frame, initial_frame):
		face = self.faces(frame)
		(x1, y1, x2, y2) = face.astype("int")

		initial_face = self.faces(initial_frame)
		(xOne, yOne, xTwo, yTwo) = initial_face.astype("int")

		x_ratio = (x2-x1)/(xTwo - xOne)
		y_ratio = (y2-y1)/(yTwo - yOne)

		return x_ratio


	def nod(self, frame, width, initial_y1):
		face = self.faces(frame)
		shape = self.landmarks(frame)
		(x1, y1, x2, y2) = face.astype("int")


		return initial_y1/width > y1/width











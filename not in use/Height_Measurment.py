#Needed Parameters
# Distance to object
#Real Height
#Focal Length
#Image Height / Resolution
#Camera Size
#Pixels in object
# From https://github.com/janki1996/ML_HeightEstimation/blob/master/fullbodydetection.py
##########################################
# ****** ML Height Estimate Project ******#
# ** Rahul Rachh    - 1401057 **#
# ** Kedar Acharya  - 1401081 **#
# ** Janki Desai    - 1401103 **#
# ** Shloak Agarwal - 1401105 **#
##########################################


# We can initialize numpy arrays from nested Python lists, and access elements using square brackets.
import numpy as np
# Wraps the python api, and uses numpy arrays for images
import cv2
import math
from cv2 import cvtColor

phi = float(input(
	"Please enter value of tilt angle (in radians):"));  # tilt angle is angle made by camera to horizontal surface


# 'def' is like a 'function' used in c++.A function is a block of organized, reusable code that is used to perform a single, related action.
# The function name is 'inside' with the parameters 'r' & 'q' and the function returns 'true' and 'false' according to the result.
def inside(r, q):
	# Using the logical operator to equate the vlaue of 'r' and 'q' respectively to variables.
	rx, ry, rw, rh = r
	qx, qy, qw, qh = q
	# def inside returns 'true' or 'false' according to the result of relational operator.
	return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


# 'def' is like a 'function' used in c++.A function is a block of organized, reusable code that is used to perform a single, related action.
# The function name is 'draw_detections' with parameters 'img'(gray scale image/video), 'rects'(rectangle paramters) & thickness(thickness of the border(predefine=2)).
# 'draw_detections' draws the rectangle around the human body that is detected with the border thickness = 2.
# Futher the function also detect the height of the human body that is detected.
def draw_detections(img, rects, thickness=2):
	# 'for' loop until the rectangle is displayed.
	for x, y, w, h in rects:
		# The HOG detector returns slightly larger rectangles than the real objects.
		# So we slightly shrink the rectangles to get a nicer output.
		pad_w, pad_h = int(0.1512 * w), int(
			0.0482 * h)  # Continuosly experimenting with the values these suggests to be the most accurate one for the measurement of height
		# Forming and displaying the rectangle.
		cv2.rectangle(img, (x + pad_w, y + pad_h), (x + w - pad_w, y + h - pad_h), (0, 255, 0), thickness)
		# 'P_ref' stands for pixel reference which is equal to total number of pixels present in height of frame (display resolution of frame is 640X480)
		P_ref = 400
		# 'H_ref' stands for height reference which is equal to height of referred person
		H_ref = 165
		# 'P_left' is the pixel that are left between the bottom of the rectangle frame and the bottom of the display screen.
		P_left = float(P_ref - float((y + h - pad_h) / math.cos(phi)));
		h = float(h / math.cos(phi));
		if (P_left < 200):
			Height = float(
				((h - (2 * pad_h)) * H_ref) / (P_ref - (2 * P_left)));  # Predicted height according to the formula.

			P_height = int(Height);
			if (P_height > 100):
				text_color = (0, 255, 0)
				if (phi != 1.57):
					cv2.putText(resized_image, str(P_height) + "cm", (x + pad_w, y + pad_h), cv2.FONT_HERSHEY_PLAIN,
								1.2, text_color, thickness=2)
					print
					float(P_height);
			print
			"Height:" + str(P_height);


# While running the python file name is changed to main

if __name__ == '__main__':

	hog = cv2.HOGDescriptor()
	hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
	cap = cv2.VideoCapture(0)  # capture real time video from camera
	# for seg
	fgbg = cv2.createBackgroundSubtractorMOG2()

	while True:
		ret, frame = cap.read()
		# for grayscale
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		# fgmask = fgbg.apply(frame)
		resized_image = cv2.resize(gray,
								   (400, 400))  # image resizing to reduce computational complexity and to increase FPS
		found, w = hog.detectMultiScale(resized_image, winStride=(8, 8), padding=(32, 32), scale=1.05)
		draw_detections(resized_image, found)
		cv2.imshow('feed', resized_image)

		ch = 0xFF & cv2.waitKey(1)
		if ch == 27:
			break

	cv2.release()
	cv2.destroyAllWindows()
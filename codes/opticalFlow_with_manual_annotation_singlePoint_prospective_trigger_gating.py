# Optical flow based detection of a single point on frame, track the point on every frame. find the distance of the every 
# detection to the reference point and check if the distance in pixels within range of the error margin, if so send trigger signal to serial arduino.
# arduino reads the value '1' and make digital output pin 13 as high for the trigger TTL input of MRI spectrometer. 
# input - realtime video
# output - TTL pulse, tracking position coordinates

import cv2
import numpy as np
from cropping_image_manualBox import crop_frame
import matplotlib.pyplot as plt
from plotting import *
import serial
import time
import os
import math

# Serial send to arduino for triggering - intialisation
serial_port = 'COM11'  
baud_rate = 9600
ser = serial.Serial(serial_port, baud_rate)

# Read time video 
cap = cv2.VideoCapture(1) # read from camera 0 or 1
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
writer = cv2.VideoWriter("./path for saving video", cv2.VideoWriter_fourcc(*'mp4v'), 30, (1280, 720))

# Grab first frame for defining tracking point
_, frame = cap.read()
first_frame = frame
old_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Lucas kanade parameters for optical flow tracking 
lk_params = dict(winSize = (20, 20),
maxLevel = 30,
criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

#selecting the point to be tracked from the first frame
_, box = crop_frame(first_frame) # function to crop the frame
x,y = box[0] # only take the first point of the box as the point to be tracked 
point_selected = True
point = ()
old_points = np.array([[x, y]], dtype=np.float32) # initial point to be tracked 
referenceX, referenceY = int(old_points[0,0]), int(old_points[0,1]) # reference position for optical triggering 
saved_point = []
start = 0 # flag for starting the video record

#checking the distance for triggering 
range_pixels = 5 # Range of pixel distance for triggering 
def is_within_range(x, y, x0, y0, range_pixels):
    # Calculate the Euclidean distance between (x, y) and (x0, y0)
    distance = math.sqrt((x - x0)**2 + (y - y0)**2)  
    # Check if the distance is within the specified range (range_pixels)
    if distance <= range_pixels:
        return True
    else:
        return False

# Optical flow loop with distance check and triggering
while True:
    _, frame = cap.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if point_selected is True:
        new_points, status, error = cv2.calcOpticalFlowPyrLK(old_gray, gray_frame, old_points, None, **lk_params)
        old_gray = gray_frame.copy()
        old_points = new_points
        x, y = new_points.ravel()
        cv2.circle(frame, (int(x), int(y)), 7, (0, 255, 0), -1) # detected points
        cv2.drawMarker(frame, (referenceX, referenceY),(0, 0, 200),cv2.MARKER_CROSS,50,2) # refernce points for triggering
        writer.write(frame) # write the frame to the file
        saved_point.append([int(x),int(y)])        
        result = is_within_range(x, y, referenceX, referenceY, range_pixels) # check for triggering range 
        
        if result is True:        
            cv2.putText(frame, "Trigger", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            ser.write(b'10')  # send '1' to arduino. check arduino code for correct serial protocol                          
            writer.write(frame)
            start = 1
        elif result is False and start == 1: # video record start at 1st trigger and continue
            writer.write(frame)

    else:
        cv2.circle(frame, (100, 100), 7, (0, 255, 0), -1)
        
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        ser.close()
        writer.release() 
        break

saved_point = np.array(saved_point)
np.save("./path for the tracked motion_trajectory.npy",saved_point)
writer.release() 
ser.close()  
cap.release()
cv2.destroyAllWindows()
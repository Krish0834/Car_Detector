import torch
import cv2
import numpy as np

# Load the pre-trained YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Define color check function
def is_blue_car(roi):
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([90, 50, 70])
    upper_blue = np.array([130, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    blue_ratio = cv2.countNonZero(mask) / (roi.shape[0] * roi.shape[1])
    return blue_ratio > 0.2

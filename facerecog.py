# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 03:02:12 2023

@author: 91892
"""

import cv2
import os
import numpy as np

# Path to the directory containing the training images
train_dir = "D:/Projects/ISM/FaceImage"

# Get a list of all the image filenames in the training directory
image_files = os.listdir(train_dir)

# Create lists to store the images and corresponding labels
images = []
labels = []

# Loop through each image file and extract the face from the image
for file in image_files:
    image_path = os.path.join(train_dir, file)
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('C:/Users/91892/haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if len(faces) != 1:
        # Skip images with no faces or more than one face
        continue
    x, y, w, h = faces[0]
    face = gray[y:y+h, x:x+w]

    # Add the face and corresponding label to the lists
    images.append(face)
    temp = file.split('.')[0]
    ind = temp.index('_')
    labels.append(int(temp[ind+1:]))
    # print(file.split('.')[0])

# Convert the lists to numpy arrays
images = np.array(images)
labels = np.array(labels)

# Train the LBPHFaceRecognizer on the images and labels
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.train(images, labels)

face_recognizer.write('D:/Projects/ISM/trained_model.yml')

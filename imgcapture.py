import cv2
import os

# pipeline = "videocapture device=0 ! video/x-raw, width=1280, height=720, framerate = 60/1 ! videoconvert ! video/x-raw, format=BGR ! appsink"

cap = cv2.VideoCapture(0)

# Check if camera is opened successfully
if not cap.isOpened():
    print("Error: Unable to access camera")
else:
    print(cap.isOpened())

# Create the output directory if it doesn't exist
output_dir = 'D:/Projects/ISM/FaceImage'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Capture and save frames from the camera
count = 0
while True:
    # Capture a frame
    ret, frame = cap.read()

    # Save the captured frame to disk in the output directory
    img_path = os.path.join(output_dir, f'image_{count}.jpg')
    cv2.imwrite(img_path, frame)

    # Display the captured frame
    cv2.imshow('frame', frame)

    # Increment the count and exit loop if maximum number of images is reached
    count += 1
    if count == 15: # set the maximum number of images to capture here
        break

    # Exit loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object and close all windows
cap.release()
cv2.destroyAllWindows()

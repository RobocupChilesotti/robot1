import cv2
import picamera2
import picamera2.array
import numpy as np

with picamera22.PiCamera() as camera:
    # Set the resolution
    camera.resolution = (640, 480)
    
    with picamera2.array.PiRGBArray(camera) as output:
        camera.capture(output, 'rgb')
        img = output.array

# Now 'img' can be used as an OpenCV image

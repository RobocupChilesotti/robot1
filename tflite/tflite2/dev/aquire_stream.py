#!/usr/bin/python3
 
import cv2
import time
from picamera2 import Picamera2
from initialize_tf import height, width


def initialize_picamera():
    cv2.startWindowThread()
     
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (width, height)}))
    picam2.start()
    
    return picam2
    
    
def get_frame(picam2):
    return cv2.cvtColor(picam2.capture_array(), cv2.COLOR_RGB2BGR)    


if __name__ == '__main__':
    # Grab images as numpy arrays and leave everything else to OpenCV.
    
    picam2 = initialize_picamera()
     
    while True:
        start_time = time.time()
        
        img = get_frame(picam2)
     
        cv2.imshow("Camera", img)
        cv2.waitKey(1)
     
        end_time = time.time()
     
        print(1 / (end_time - start_time))

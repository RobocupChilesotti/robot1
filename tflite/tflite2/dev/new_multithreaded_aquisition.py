import threading
import cv2
from libcamera import controls
import time
from picamera2 import Picamera2
from initialize_tf import height, width


normalSize = (640, 480)
lowresSize = (width, height)

rectangles = []

   
cv2.startWindowThread()
    
picam2 = Picamera2()
picam2.set_controls({"AwbEnable": True})
picam2.set_controls({"AwbMode": controls.AwbModeEnum.Cloudy})
#picam2.set_controls({"FrameRate": 1.0})
config = picam2.create_preview_configuration(main={"size": (width, height)},
                                                lores={"size": lowresSize, "format": "YUV420"})
# config["transform"] = libcamera.Transform(hflip=1, vflip=1)
picam2.configure(config)

picam2.start()


global frame
frame = cv2.cvtColor(picam2.capture_array("lores"), cv2.COLOR_YUV420p2RGB)


def foto():
    while True:
        frame = cv2.cvtColor(picam2.capture_array("lores"), cv2.COLOR_YUV420p2RGB)
        
        # Define the RGB color you want to use
        color = (255, 0, 0)  # Red color

        wall_height = 170

        # Fill the upper half of the image with the defined color
        frame[0:height - wall_height, :] = color
        
        frame = frame[:,:320]

# Create a Thread object.
thread = threading.Thread(target=foto)

# Start the thread.
thread.start()


if __name__ == '__main__':
    # Print the result.
    while True:
        cv2.imshow('frame', frame)
        cv2.waitKey(1)














'''

def get_frame():
    frame = cv2.cvtColor(picam2.capture_array("lores"), cv2.COLOR_YUV420p2RGB)
    
    # Define the RGB color you want to use
    color = (255, 0, 0)  # Red color

    wall_height = 170

    # Fill the upper half of the image with the defined color
    frame[0:height - wall_height, :] = color
    
    return frame[:,:320]


if __name__ == '__main__':
    # Grab images as numpy arrays and leave everything else to OpenCV.
    
    while True:
        start_time = time.time()
        
        #img = get_frame_old(picam2)

        rgb = get_frame()

        cv2.imshow("Camera", rgb)
        cv2.waitKey(1)
     
        end_time = time.time()
     
        print(1 / (end_time - start_time))

        
'''
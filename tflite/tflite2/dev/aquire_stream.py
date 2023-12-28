#!/usr/bin/python3
 
import cv2
import time
import libcamera
from picamera2 import MappedArray, Picamera2, Preview
from initialize_tf import height, width


normalSize = (640, 480)
lowresSize = (320, 240)

rectangles = []


def DrawRectangles(request):
    with MappedArray(request, "main") as m:
        for rect in rectangles:
            rect_start = (int(rect[0] * 2) - 5, int(rect[1] * 2) - 5)
            rect_end = (int(rect[2] * 2) + 5, int(rect[3] * 2) + 5)
            cv2.rectangle(m.array, rect_start, rect_end, (0, 255, 0, 0))


def initialize_picamera():
    cv2.startWindowThread()
     
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(lores={"size": (width, height)}, buffer_count=1)
    #config = picam2.create_preview_configuration(main={"size": (width, height)},
    #                                             lores={"size": lowresSize, "format": "YUV420"})
    #config["transform"] = libcamera.Transform(hflip=1, vflip=1)
    picam2.configure(config)

    #picam2.set_controls({"FrameRate": 40})

    '''
    stride = picam2.stream_configuration("lores")["stride"]
    picam2.post_callback = DrawRectangles
    '''
    stride = ''

    picam2.start()
    
    return picam2, stride, width
    
    
def get_frame(picam2):
    frame = cv2.cvtColor(picam2.capture_array("lores"), cv2.COLOR_YUV420p2RGB)
    return frame[:,:320]


def get_frame_(picam2):
    buffer = picam2.capture_buffer("lores")
    grey = buffer[:stride * lowresSize[1]].reshape((lowresSize[1], stride))
    return grey[:,:width]


if __name__ == '__main__':
    # Grab images as numpy arrays and leave everything else to OpenCV.
    
    picam2, stride, width = initialize_picamera()
     
    while True:
        start_time = time.time()
        
        img = get_frame(picam2)

        #grey = get_frame(picam2)

        cv2.imshow("Camera", img)
        cv2.waitKey(1)
     
        end_time = time.time()
     
        print(1 / (end_time - start_time))

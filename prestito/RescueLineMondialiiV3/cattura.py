#import RescueLineParabola

import os
import argparse
import cv2
import numpy as np
import sys
import time
from threading import Thread
import importlib.util
#from gap import gap
#from prava import a

#import prova2

global immagine
immagine=np.zeros(shape=(148,148),dtype=np.uint8)

global TipoStream
TipoStream=0


def foto():
    img = immagine.copy()
    if (TipoStream==1):
        img=img[14:142,14:142]
        #img[14:142,14:142,0]=255
    return img



class VideoStream:
    """Camera object that controls video streaming from the Picamera"""
    def __init__(self,resolution=(640,480),framerate=30,saturation = 100,contrast= 70):
        # Initialize the PiCamera and the camera image stream
        self.stream = cv2.VideoCapture(0)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3,resolution[0])
        ret = self.stream.set(4,resolution[1])
        #ret = self.stream.set(10,500)
        #ret = self.stream.set(12, cv2.CAP_PROP_SATURATON=100)
        #ret = self.stream.set(17,10)
            
        # Read first frame from the stream
        #(self.grabbed, self.frame) = self.stream.read()

    # Variable to control when the camera is stopped
        self.stopped = False

    def start(self):
    # Start the thread that reads frames from the video stream
        Thread(target=self.update,args=()).start()
        return self

    def update(self):
        # Keep looping indefinitely until the thread is stopped
        while True:
            # If the camera is stopped, stop the thread
            if self.stopped:
                # Close camera resources
                self.stream.release()
                return

            # Otherwise, grab the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()
            global immagine
            immagine=self.frame.copy()
            
    def read(self):
    # Return the most recent frame
        print(id(self.frame))
        return self.frame
    
    def readid(self):
    # Return the most recent frame
        address=id(immagine)
        address2=id(self.frame)
        print (hex(address),hex(address2))
        return address

    def stop(self):
    # Indicate that the camera and thread should be stopped
        self.stopped = True
        

def avvioStream128():
    global TipoStream
    TipoStream=1
    global videostream
    videostream = VideoStream(resolution=(148,168),framerate=30,saturation = 100,contrast= 70).start()
    time.sleep(1)

def avvioStreamHD():
    global TipoStream
    TipoStream=0
    global videostream
    videostream = VideoStream(resolution=(800,600),framerate=30).start()
    time.sleep(1)
    
def stopStream():
    global videostream
    videostream.stop()
    #VideoStream().stop()
    time.sleep(1)


'''
while 1:
    a()


    
    cv2.imshow('Object detector', immagine)
    #time.sleep(0.1)
    if cv2.waitKey(1) == ord('q'):
        break
    




while 1:
    videostream.readid()
    #time.sleep(1)




#a(img=foto())

videostream.stop()
time.sleep(1)




videostream = VideoStream(resolution=(800,600),framerate=30).start()
time.sleep(1)


for i in range(1000):
    img=foto()
    cv2.imshow(img)






#stanza

videostream.stop()
time.sleep(1)




videostream = VideoStream(resolution=(64,64),framerate=30).start()
time.sleep(1)

rescueLine()

videostream.stop()
time.sleep(1)
'''

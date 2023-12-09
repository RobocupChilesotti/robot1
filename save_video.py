#!/usr/bin/python3
 
import cv2
from picamera2 import Picamera2

  
cv2.startWindowThread()
    
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (1920, 1080)}))
picam2.start()

   
# Below VideoWriter object will create 
# a frame of above defined The output  
# is stored in 'filename.avi' file. 
result = cv2.VideoWriter('/saved_vids/picam3.avi',  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         10, (1920, 1080))
    
while(True): 
    #frame = cv2.cvtColor(picam2.capture_array(), cv2.COLOR_RGB2RGB)
    frame = picam2.capture_array()


  
    # Write the frame into the 
    # file 'filename.avi' 
    result.write(frame) 

    # Display the frame 
    # saved in the file 
    cv2.imshow('Frame', frame) 

    # Press S on keyboard  
    # to stop the process 
    if cv2.waitKey(1) & 0xFF == ord('s'): 
        break

  
# When everything done, release  
# the video capture and video  
# write objects 
result.release() 
    
# Closes all the frames 
cv2.destroyAllWindows() 
   
print("The video was successfully saved") 
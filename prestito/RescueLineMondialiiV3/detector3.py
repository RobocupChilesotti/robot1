import cv2
import logging
import datetime
import time
import edgetpu.detection.engine
from PIL import Image
from cattura import foto

from cattura import foto
import numpy as np
#from stampa import stampa
from threading import Thread



#model='/home/pi/Downloads/output_tflite_graph_edgetpu.tflite'
model = '/home/pi/Downloads/ssdlite_mobiledet_mask_edgetpu (5).tflite'

width=800
height=600

# initial edge TPU engine
logging.info('Initialize Edge TPU with model %s...' % model)
engine = edgetpu.detection.engine.DetectionEngine(model)
min_confidence = 0.6
#min_confidence = 0.3
num_of_objects = 5
logging.info('Initialize Edge TPU with model done.')




def palline():
    frame=foto()
    logging.debug('Detecting objects...')
    
    # call tpu for inference
    start_ms = time.time()
    frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(frame_RGB)
    objects = engine.detect_with_image(img_pil, threshold=min_confidence, keep_aspect_ratio=False,
                                     relative_coord=False, top_k=num_of_objects)

    
    
    bianca=(0,0)
    nera=(0,0)
    ostacolo=(0,0)
    
    maxBianca=0
    maxNera=0
    maxOstacolo=0
    maxBiancaX=0
    
    
    if objects:
        for obj in objects:
            
            TipoPallina= obj.label_id
            score= obj.score
            
            box = obj.bounding_box
            ymin = int(box[0][1])
            xmin = int(box[0][0])
            ymax = int(box[1][1])
            xmax = int(box[1][0])
            
            x=(xmax+xmin)/2
            
            if(TipoPallina == 2):
                y=ymax
            else:
                deltaX = 400-x
                if(deltaX<0):
                    deltaX = -deltaX
                y = (ymax+ymin)/2
                yDis=np.clip(y - deltaX//6,0,600)
                
            
            
            
            if(TipoPallina==0):
                #pallina bianca
                if(yDis>maxBianca):
                    bianca=(y,x)
                    maxBianca = yDis
                    maxBiancaX = x
            else:
                if(TipoPallina==1):
                    #pallina nera
                    if(score>maxNera):
                        nera=(y,x)
                        maxNera = score
                        
                
                
                else:
                    #ostacolo
                    if(score>maxOstacolo):
                        ostacolo=(y,x)
                    
            
            cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)
            
            
        cv2.circle(frame,(int(maxBiancaX),int(maxBianca)),7,(255,0,0),thickness=2)
        cv2.circle(frame,(int(bianca[1]),int(bianca[0])),10,(255,255,0),thickness=2)
        return frame, bianca, nera, ostacolo
    else:
        #logging.debug('No object detected')
        return frame, bianca, nera, ostacolo
    #cv2.imshow('Detected Objects', frame)

    #return frame



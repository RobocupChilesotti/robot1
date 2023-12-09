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


model='/home/pi/Desktop/full TPU+ new verde/modello/razzismo.tflite'
label='/home/pi/Desktop/full TPU+ new verde/modello/labels_map.txt'
width=800
height=600

# initialize TensorFlow models
with open(label, 'r') as f:
    pairs = (l.strip().split(maxsplit=1) for l in f.readlines())
    labels = dict((int(k), v) for k, v in pairs)

# initial edge TPU engine
logging.info('Initialize Edge TPU with model %s...' % model)
engine = edgetpu.detection.engine.DetectionEngine(model)
min_confidence = 0.30
num_of_objects = 3
logging.info('Initialize Edge TPU with model done.')

# initialize open cv for drawing boxes
font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10, height - 10)
fontScale = 1
fontColor = (255, 255, 255)  # white
boxColor = (0, 0, 255)  # RED
boxLineWidth = 1
lineType = 2
annotate_text = ""
annotate_text_time = time.time()
time_to_show_prediction = 1.0  # ms




def detect_objects(frame):
    logging.debug('Detecting objects...')

    # call tpu for inference
    start_ms = time.time()
    frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(frame_RGB)
    objects = engine.detect_with_image(img_pil, threshold=min_confidence, keep_aspect_ratio=True,
                                     relative_coord=False, top_k=num_of_objects)
    
    ymax_max=0
    
    
    
    if objects:
        for obj in objects:
            
            box = obj.bounding_box
            ymin = int(box[0][1])
            xmin = int(box[0][0])
            ymax = int(box[1][1])
            xmax = int(box[1][0])
            
            TipoPallina= obj.label_id

            cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)
            
            deltaX=(400-(xmax+xmin)/3)/20
            
            if(deltaX<0):
                deltaX=-deltaX
                
            deltaX=20-deltaX
            
            if(ymax+deltaX>ymax_max):
                ymax_max=ymax+deltaX
                pallinaVicina=obj.bounding_box
                TipoPallinaDef=TipoPallina
            
            
            '''
            height = obj.bounding_box[1][1]-obj.bounding_box[0][1]
            width = obj.bounding_box[1][0]-obj.bounding_box[0][0]
            logging.debug("%s, %.0f%% w=%.0f h=%.0f" % (labels[obj.label_id], obj.score * 100, width, height))
            box = obj.bounding_box
            
            x
            
            
            coord_top_left = (int(box[0][0]), int(box[0][1]))
            coord_bottom_right = (int(box[1][0]), int(box[1][1]))
            print(coord_top_left)
            cv2.rectangle(frame, coord_top_left, coord_bottom_right, boxColor, boxLineWidth)
            annotate_text = "%s %.0f%%" % (labels[obj.label_id], obj.score * 100)
            coord_top_left = (coord_top_left[0], coord_top_left[1] + 15)
            cv2.putText(frame, annotate_text, coord_top_left, font, fontScale, boxColor, lineType)
            '''
        box = pallinaVicina
        ymin = int(box[0][1])
        xmin = int(box[0][0])
        ymax = int(box[1][1])
        xmax = int(box[1][0])
        
        cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (255, 10, 0), 2)
        
        posX=(xmax+xmin)/2
        posY=(ymin+ymax)/2
        
        dim=(xmax-xmin)*(ymax-ymin)
        
        return frame, 1,(posY,posX),dim,TipoPallinaDef
    else:
        #logging.debug('No object detected')
        return frame, 0,(0,0),0,0
    #cv2.imshow('Detected Objects', frame)

    #return frame


def palline():
    img=foto()
    img=cv2.circle(img,(50,450),45,(0,0,255),thickness=-1)
    img=cv2.circle(img,(750,450),45,(0,0,255),thickness=-1)
    img2,stato,pos,dim,tipo=detect_objects(img)
    #cv2.imshow('img',img2)
    #stampa(img2,(400,300),'camera')
    
    return stato,pos,dim,img2,tipo


def analizzaImmagine(coso):
    img=coso.copy()
    img2,stato,pos,dim=detect_objects(img)
    #stampa(img2,(800,600),'camera')
    return stato,pos


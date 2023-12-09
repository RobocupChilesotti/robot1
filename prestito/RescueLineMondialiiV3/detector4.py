from cattura import avvioStreamHD
from pycoral.adapters import common 
from pycoral.adapters import detect 
from pycoral.utils.dataset import read_label_file 
from pycoral.utils.edgetpu import make_interpreter 
import cv2
import time
from PIL import Image
from cattura import foto
import numpy as np
from threading import Thread


def draw_objects(draw, objs, labels): 
  """Draws the bounding box and label for each object.""" 
  for obj in objs: 
    bbox = obj.bbox 
    draw.rectangle([(bbox.xmin, bbox.ymin), (bbox.xmax, bbox.ymax)], 
                   outline='red') 
    draw.text((bbox.xmin + 10, bbox.ymin + 10), 
              '%s\n%.2f' % (labels.get(obj.id, obj.id), obj.score), 
              fill='red') 
 
 

model = '/home/pi/Downloads/ssdlite_mobiledet_mask_edgetpu (5).tflite'
interpreter = make_interpreter(model) 
interpreter.allocate_tensors() 
min_confidence = 0.5

def palline():
    frame = foto()
    
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    image = Image.fromarray(frame)
    _, scale = common.set_resized_input( interpreter, image.size, lambda size: image.resize(size, Image.ANTIALIAS)) 

    interpreter.invoke()
    objects = detect.get_objects(interpreter, min_confidence, scale)



    
    bianca=(0,0)
    nera=(0,0)
    ostacolo=(0,0)
    
    maxBianca=0
    maxNera=0
    maxOstacolo=0
    maxBiancaX=0
    
    
    if objects:
        for obj in objects:
            
            TipoPallina = obj.id
            score = obj.score
            bbox = obj.bbox 
            ymin = bbox.ymin
            xmin = bbox.xmin
            ymax = bbox.ymax
            xmax = bbox.xmax
            
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

if(__name__ == '__main__'):
    avvioStreamHD()
    time.sleep(1)
    #cv2.imshow('img',foto())
    #cv2.waitKey(0)
    while 1:
        tin = time.time()
        img,b,n,o=palline()
        print('fps:',1/(time.time()-tin))
        print(b,n,o)
        cv2.imshow('img',img)
        cv2.waitKey(1)&0xff

#from detector2 import palline
from detector3_1 import palline as palline3
from cattura import avvioStreamHD
import cv2
import time
avvioStreamHD()
#CameraSU()


tipo=1

while(1):
    t1=time.time()
    if (tipo==0):
        stato,posizione,dim,img,tipo=palline()
        #img=cv2.resize(img,(800,600))
        img=cv2.circle(img,(int(posizione[1]),int(posizione[0])),20,(255,0,0),4)
        print(posizione,dim,stato,tipo)
    else:
        img,b,n,o,bu=palline3()
        print(b,n,o)
        
        deltaXo = o[1]-b[1]
        deltaYo = o[0]-b[0]
        #if(b==(0,0)):
            #print('no bianca')
        if(deltaXo<0):
            deltaXo=-deltaXo
        
        #print(deltaYo,deltaXo)
    cv2.imshow('img',img)
    cv2.waitKey(1)&0xff
    print(1/(time.time()-t1))
    
    
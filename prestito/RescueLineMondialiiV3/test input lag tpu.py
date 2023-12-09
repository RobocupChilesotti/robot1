from detector4 import palline
from cattura import avvioStreamHD
from cattura import foto
import cv2
import time
import numpy as np
#from threading import thread
from threading import Thread
from robot import Vmotori
avvioStreamHD()
#CameraSU()


tipo=1
nPre = (0,0)
NpixelPre = 0
#Vmotori(30,30)

def threadimgN():
    NpixelPre = 0
    global Tcamera
    Tcamera = 0
    while 1:
        img = foto()
        img2 =cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret,th1 = cv2.threshold(img2[200:400,200:600],60,255,cv2.THRESH_BINARY)
        Npixel = np.count_nonzero(255-th1)

        if(NpixelPre>1000 and Npixel <1000):
            print('pallina persa da camera a:',time.time())
            Tcamera = time.time()
            #Vmotori(0,0)
            #time.sleep(1)
            #Vmotori(30,40)
        NpixelPre = Npixel

    
        

T=Thread(target=threadimgN,args=())
#T.start()

global Tcamera
Tcamera = 0
while(1):
        
        img,b,n,o=palline()
        img2 =cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret,th1 = cv2.threshold(img2[200:400,200:600],60,255,cv2.THRESH_BINARY)
        Npixel = np.count_nonzero(255-th1)
        
        #print(b,n,o)
        
        if(nPre!=(0,0) and n==(0,0)):
            print('pallina persa da object a:',time.time())
            print('deltaT:',time.time()-Tcamera)
            
        #if(NpixelPre>1000 and Npixel <1000):
        #    print('pallina persa da camera a:',time.time())
        
        #NpixelPre = Npixel
        nPre = n
        '''
        nera = n
        
        ErroreY = 200-nera[0]
                            
      
        ErroreX = 400-nera[1]
     
        
        Ky=0.3
        Kx=0.2
        
        Vsx=ErroreY*Ky+ErroreX*Kx
        Vdx=ErroreY*Ky-ErroreX*Kx
        
        Vsx=np.clip(Vsx,-30,30)
        Vdx=np.clip(Vdx,-30,30)
        Vmotori(Vsx,Vdx)
        
                          
                            
        '''
        #print(deltaYo,deltaXo)
        cv2.imshow('img',img[200:400,200:600])
        #cv2.imshow('img',img)
        cv2.waitKey(1)&0xff
        
    #print(1/(time.time()-t1))
    
    
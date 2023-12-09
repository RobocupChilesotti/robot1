import cv2
import numpy as np
from robot import Vmotori
from cattura import foto
from Semplifica import semplifica
import time
from robot import ControlloPinza
from robot import BraccioSuCubo
from robot import BraccioSuCubo2
from robot import BraccioGiuCubo
from robot import PinzaSX
from robot import PinzaDX
from robot import BraccioImmezzoCubo
from robot import PinzaRelax
def cuboblu():
    print('cubo blu')
    
    Cpersi = 0
    arrayTime = np.zeros(shape = (10000),dtype = np.float64)
    arrayVel = np.zeros(shape = (10000,2),dtype = np.int16)
    c = 0
    cPre = 0
    Cvicini = 0
    Tin = time.time()
    while 1:
        
        if(time.time()-Tin>10):
            break
        
        img = foto()
        mask,r,g,b,s = semplifica(img)
        
        B = img[:,:,0]
        B[b == 255] = 255
        img[:,:,0] = B
        cv2.imshow('b',b)
        cv2.imshow('img',img)
        cv2.waitKey(1)&0xff
        
        M = cv2.moments(b)
        if(M["m00"]!=0):
            Cpersi = 0
            cX = int(M["m10"] / M["m00"])-64
            cY = -int(M["m01"] / M["m00"])+32

            

            if(c!=cPre):
                cPre = c
                T = time.time()-Tin
                arrayTime[c-1] = T

            dx = cY*1-cX*1
            sx = cY*1+cX*1
            print (cX,cY,dx,sx)
            Vmotori(dx,sx)
            Tin = time.time()
            
            if(cY>-7 and cY<7 and cX>-7 and cX<7):
                Cvicini+=1
                if(Cvicini > 20):
                    break
            else:
                Cvicini=0
                arrayVel[c,0] = dx
                arrayVel[c,1] = sx
                c+=1

        else:
            Cpersi+=1
            
            if(Cpersi>30):
                break
    
    
    if(Cvicini>20):
        Vmotori(-30,-30)
        time.sleep(1)
        Vmotori(0,0)
        BraccioGiuCubo()
        #metto i becchi bene
        PinzaRelax()
        #ControlloPinza()
        Vmotori(20,20)
        time.sleep(0.5)
        Vmotori(0,0)
        #chiudo la pinza
        for i in range(80,0,-1):
            PinzaSX(i)
            PinzaDX(i)
            time.sleep(0.005)
    
        time.sleep(0.3)

        BraccioSuCubo()


        time.sleep(0.3)
            
        # scarico lato bianca
        for i in range(30,100,1):
            PinzaSX(i)
            #PinzaDX(i)
            time.sleep(0.005)
        
        time.sleep(1)
        
        for i in range(30,100,1):
            #PinzaSX(i)
            PinzaDX(i)
            time.sleep(0.005)
        time.sleep(0.5)
        BraccioImmezzoCubo()
        #BraccioGiuCubo()
        #ControlloPinza()
        #BraccioSuCubo2()
        PinzaRelax()
        
        

    for i in range(c,0,-1):
        Vmotori(-arrayVel[i,0],-arrayVel[i,1])
        time.sleep(arrayTime[i])
        
        
    Vmotori(0,0)




if (__name__ == '__main__'):
    from cattura import avvioStream128
    avvioStream128()
    cuboblu()
    
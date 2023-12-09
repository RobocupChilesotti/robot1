import cv2
import numpy as np

                     # B   G   R
                     # V   S   H
#hsw valori su immagini
#R=V  quanto e chiaro
#G=S  saturazione
#B=H  angolo o tipo colore
                      #B  G   R     
                      #H  S   V  
lower_blue = np.array([90,70,70])
upper_blue = np.array([130,255,230])
                      #B  G   R                    
                      #H  S   V                                         
lower_green = np.array([40,100,25]) 
upper_green = np.array([87,255,230])
                      #B  G   R     
                      #H  S   V  
lower_red = np.array([0,150,90])
upper_red = np.array([20,255,220])
                      #B  G   R     
                      #H  S   V  
lower_red2 = np.array([130,150,90])
upper_red2 = np.array([255,255,220])
                      #B  G   R     
                      #H  S   V  
lower_silver = np.array([0,0,210])
upper_silver = np.array([255,70,255])

kernel = np.ones((5,5),np.uint8)

kernel2 = np.ones((15,15),np.uint8)

correzione=cv2.imread('/home/pi/Desktop/correzione luci.png')

correzioneTH=correzione[:,:,0]

ret ,correzioneTH = cv2.threshold(correzioneTH,190,255,cv2.THRESH_BINARY)

correzioneTH=correzioneTH//255

#cv2.imshow('correzioneTH',correzioneTH)
#cv2.waitKey(0)

correzione=255-correzione
correzione=np.uint8(correzione/3)

imgW=np.ones((128,128),dtype=np.uint8)*255
imgB=np.zeros((128,128),dtype=np.uint8)

kernelBordi=np.ones((2,2),dtype=np.uint8)

def semplifica(img2):
    
    
    
    hsv = cv2.cvtColor(img2,cv2.COLOR_BGR2HSV)
    
    #silver = cv2.inRange(hsv, lower_silver, upper_silver)
    silver=cv2.Canny(hsv[:,:,2],100,150)
    
    
    silver=cv2.dilate(silver,kernel,iterations=1)
    silver=cv2.erode(silver,kernel,iterations=2)
    
    hsv = cv2.medianBlur(hsv,5)
    
    
    cv2.imshow('hsv',hsv)
    
    #hsv2 = cv2.resize(hsv,(600,600))
    #cv2.imshow('hsv2',hsv2)
    # blu
    blu = cv2.inRange(hsv, lower_blue, upper_blue)

    # verde
    verde = cv2.inRange(hsv, lower_green, upper_green)

    #rosso
    rosso = cv2.inRange(hsv, lower_red, upper_red)
    
    #rosso2
    rosso2 = cv2.inRange(hsv, lower_red2, upper_red2)
    
    rosso=rosso+rosso2
    
    
    
    
    rosso = cv2.morphologyEx(rosso, cv2.MORPH_OPEN, kernel)
    verde = cv2.morphologyEx(verde, cv2.MORPH_OPEN, kernel)
    blu = cv2.morphologyEx(blu, cv2.MORPH_OPEN, kernel)
    
    

    #cv2.imshow('verde',verde)
    

    img2=np.int16(img2)
    #print(np.shape(img2))
    img2-=correzione
    img2=np.clip(img2,0,255)
    img2=np.uint8(img2)


    #cv2.imshow('preblur',img2)
    img2=cv2.medianBlur(img2,5)
    #cv2.imshow('blur',img2)  
    

    cv2.imshow('imgTrattata',img2)
    
    img2=cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)

    

    

    #img2[verde == 255] = 200

    #cv2.imshow('imgTrattata2',img2)

    #th2 = cv2.adaptiveThreshold(img2,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,61,40)
    '''
    ret,th1 = cv2.threshold(img2,60,255,cv2.THRESH_BINARY)
    ret,th2 = cv2.threshold(img2,40,255,cv2.THRESH_BINARY)
    
    if(np.count_nonzero(th2[70:128,:]*correzioneTH[70:128,:]<100)):
        ret,th1 = cv2.threshold(img2,40,255,cv2.THRESH_BINARY)
        ret,th2 = cv2.threshold(img2,30,255,cv2.THRESH_BINARY)
    
    th2=th1*correzioneTH+th2*(1-correzioneTH)
    '''
    ret,th1 = cv2.threshold(img2,80,255,cv2.THRESH_BINARY)
    
    th1=th1[60:127,:]
    
    #th2 = cv2.adaptiveThreshold(img2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,91,15)
    th2 = cv2.adaptiveThreshold(img2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,121,16)
    
    
    th2[60:127,:]=th1
    
    if(np.count_nonzero(rosso)>10):
        th2[rosso==255]=255
    
    if(np.count_nonzero(verde)>10):
        th2[verde==255]=255
    
    #print(np.shape(correzioneTH))
    th2=cv2.erode(th2,kernel,iterations=1)
    th2=cv2.dilate(th2,kernel,iterations=1)
    
    
    
    return th2, rosso, verde , blu, silver
    
    '''
    cv2.imshow('bordi',bordi)
    amount, labels = cv2.connectedComponents(bordi)

    #print(amount)


    mask=imgW.copy()
    #R=imgB.copy()
    #G=imgB.copy()
    #B=imgB.copy()
    for i in range(1,amount):
        
        maskArea=imgB.copy()
        maskArea[labels == i] = 1
        #cv2.imshow('maskArea',maskArea*255)
        #cv2.waitKey(0) 
        #areaG=verde*maskArea
        #areaB=blu*maskArea
        #areaR=rosso*maskArea
        areaW=th3*maskArea
        #linea
        areaL=(255-th3)*maskArea
        #cv2.imshow('areaL',areaL)
        #cv2.waitKey(0) 
        #calcolo quale colore vale in quest area
        #pointG=np.count_nonzero(areaG)*2.5
        #pointB=np.count_nonzero(areaB)*2.5
        #pointR=np.count_nonzero(areaR)*2.5
        pointW=np.count_nonzero(areaW)
        pointL=np.count_nonzero(areaL)
        
        if(pointL>pointW):
            mask-=maskArea
            
        
        
        pointR=0
        pointB=0
        
        pointMax=np.amax((pointG,pointB,pointR,pointW,pointL))
        
        #print(pointMax,pointG)
        
        maskArea*=255
        #cv2.imshow('maskArea',maskArea)
        #cv2.waitKey(0)
        if(pointW!=pointMax):
            if(pointL==pointMax):
                mask-=maskArea
                
            else:
                if(pointG==pointMax):
                    G+=maskArea
                
                else:
                    if(pointB==pointMax):
                        B+=maskArea
                
                    else:
                        
                        if(pointR==pointMax):
                           R+=maskArea
            
                    
        '''
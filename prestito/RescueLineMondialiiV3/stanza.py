import cv2
import numpy as np

from robot import Vmotori
from cattura import foto
from Semplifica import semplifica
from cattura import avvioStream128
from cattura import avvioStreamHD
from cattura import stopStream
from robot import cameraSu
from robot import cameraGiu
import time

#cameraSu()
avvioStreamHD()

sigma=10



def sx90():
    Vmotori(30,-30)
    time.sleep(2)
    Vmotori(0,0)
    return

def dx90():
    Vmotori(-30,30)
    time.sleep(2.3)
    Vmotori(0,0)
    return
    

def undesired_objects (image):
    image = image.astype('uint8')
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(image, connectivity=4)
    sizes = stats[:, -1]

    max_label = 1
    max_size = sizes[1]
    for i in range(2, nb_components):
        if sizes[i] > max_size:
            max_label = i
            max_size = sizes[i]

    img2 = np.zeros(output.shape)
    img2[output == max_label] = 255
    
    return img2
    #cv2.imshow("Biggest component", img2)
    #cv2.waitKey()
    



imgB=np.zeros((600,800),dtype=np.uint8)

while 1:
    
    
    t1=time.time()
    
    img=foto()
    
    
    
    gray = cv2.cvtColor(img[200:400,500:800], cv2.COLOR_BGR2GRAY)
    #CV_8UC1
    laplacian = cv2.Laplacian(gray,cv2.CV_32F,ksize=1)
    laplacian = cv2.blur(laplacian,(5,5))
    laplacian = np.clip(laplacian,0,1)
    
    
    laplacian = np.uint8(laplacian*255)
    
    
    #laplacian = cv2.morphologyEx(laplacian, cv2.MORPH_CLOSE, kernel)
    laplacian = cv2.blur(laplacian,(5,5))
    
    #bordi = cv2.Canny(laplacian,50,200)
    bordi = cv2.adaptiveThreshold(255-laplacian,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,101,50)
    kernel = np.ones((5,5),np.uint8)
    bordi = cv2.erode(bordi,kernel,iterations = 3)
    

    area= undesired_objects(bordi)

    #print(1/(time.time()-t1))

    kernel = np.ones((25,25),np.uint8)

    area = cv2.morphologyEx(area, cv2.MORPH_CLOSE, kernel)

    imgMezzi=img[200:400,500:800]
    
    imgMezzi[area==255,1]=255
    
    img[200:400,500:800]=imgMezzi
    
    img=cv2.rectangle(img,(700,200),(785,400),(0,0,255),thickness=1)
    #img=cv2.rectangle(img,(15,200),(100,400),(0,0,255),thickness=1)
    
    img=cv2.rectangle(img,(500,200),(600,300),(255,0,0),thickness=1)
    
    sogliaDX=area[:,200:285]
    
    sogliaH=area[0:100,200:600]
    
    
    NareaH=(9375-np.count_nonzero(sogliaH))/93
    
    print(np.count_nonzero(sogliaH))
    NareaDX=(10000-np.count_nonzero(sogliaDX))/100/4
    
    Vmotori(30+NareaDX+NareaH,30-NareaDX-NareaH)
    
    
    
    cv2.imshow('img',img)
    cv2.imshow('sogliaDX',sogliaDX)
    #cv2.imshow('sogliaSX',sogliaSX)
    #cv2.imshow('sogliaH',sogliaH)
    #cv2.imshow('area',area)
                                    


    cv2.waitKey(1)&0xff
    
    print(1/(time.time()-t1))
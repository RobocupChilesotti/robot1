from cattura import foto
from Semplifica import semplifica
from cattura import avvioStream128
from cattura import avvioStreamHD
from cattura import stopStream
#from robot import cameraGiu
import cv2

#cameraGiu()
avvioStream128()
#avvioStreamHD()

img=foto()
cv2.imwrite('pavNero.png',img)

while 1:
    img=foto()
    cv2.imshow('og',img)
    
    mask,r,g,b,s=semplifica(img)
    cv2.imshow('mask',mask)
    cv2.imshow('r',r)
    cv2.imshow('g',g)
    cv2.imshow('b',b)
    cv2.imshow('s',s)
    
    cv2.waitKey(1)&0xff
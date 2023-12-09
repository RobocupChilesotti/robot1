import RPi.GPIO as GPIO
import time
import numpy as np
import logging
import sys
import time
from robot import Vmotori
#from robot import resetBNO

import serial
import adafruit_bno055

#resetBNO()

time.sleep(1)

uart = serial.Serial("/dev/serial0")
sensor = adafruit_bno055.BNO055_UART(uart)


def distanzaAngolare(x1,x2):
    distanza=x1-x2
    while(distanza>180 or distanza <-180):
        if(distanza>180):
            distanza-=360
            
        if(distanza<-180):
            distanza+=360
            
    return(distanza)


global valPre
valPre = 0
def readGyroYaw():
    global valPre
    try:
        val = sensor.euler[0] + valCorrezione
        valPre = val
        return val
    except:
        Vmotori(0,0)
        print('uart error')
        time.sleep(0.5)
        return valPre
        



def giraDi(val):

    angolo=readGyroYaw()+val
    
    if(angolo>360):
        angolo-=360

    if(angolo<0):
        angolo+=360
    
    print(angolo)
    
    print(distanzaAngolare(readGyroYaw(),angolo))
    
    while 1:
        a=readGyroYaw()
        delta=distanzaAngolare(a,angolo)
        print(a,delta)
        #print(delta)
        delta*=10
        delta=np.clip(delta,-40,40)
        Vmotori(delta,-delta)
        if(delta>-20 and delta<20):
            break
    print('errore giro:',delta)
    Vmotori(0,0)
   


while (1):
    giraDi(90)

import RPi.GPIO as GPIO
import time
import numpy as np
from threading import Thread
from cattura import foto
from cattura import avvioStreamHD
import cv2
import logging
import sys
import time
#from detector4 import palline


bnoStato = 0
if(bnoStato):
    from Adafruit_BNO055 import BNO055
    bno = BNO055.BNO055(serial_port='/dev/serial0', rst=25)

    # Enable verbose debug logging if -v is passed as a parameter.
    if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
        logging.basicConfig(level=logging.DEBUG)

    # Initialize the BNO055 and stop if something went wrong.
    if not bno.begin():
        raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

    # Print system status and self test result.
    status, self_test, error = bno.get_system_status()
    print('System status: {0}'.format(status))
    print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
    # Print out an error if system status is in error mode.
    if status == 0x01:
        print('System error: {0}'.format(error))
        print('See datasheet section 4.3.59 for the meaning.')


#IO.setmode(IO.BOARD)
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#distance sensors
triggerAV = 6
echoAV = 5

buzzer = 21
P3pin = 20


triggerDX = 13
echoDX = 12


triggerSX = 19
echoSX = 16

#PinResetBno = 25

GPIO.setwarnings(False)


#GPIO.setup(PinResetBno, GPIO.OUT)
#GPIO.output(PinResetBno, False)
'''
def resetBNO():
    GPIO.output(buzzer, True)
    time.sleep(0.3)
    GPIO.output(buzzer, False)
    time.sleep(0.1)

'''
#buzzer e P3
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(P3pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def playSound():
    for i in range(300):
        GPIO.output(buzzer, True)
        time.sleep(0.001)
        GPIO.output(buzzer, False)
        time.sleep(0.001)


#set GPIO for distance sensors
GPIO.setup(triggerAV, GPIO.OUT)
GPIO.setup(echoAV, GPIO.IN)


GPIO.setup(triggerDX, GPIO.OUT)
GPIO.setup(echoDX, GPIO.IN)

GPIO.setup(triggerSX, GPIO.OUT)
GPIO.setup(echoSX, GPIO.IN)

def distanceAV():
    # set Trigger to HIGH
    GPIO.output(triggerAV, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(triggerAV, False)

    StartTime = time.time()
    StopTime = time.time()
    Tin=time.time()
    # save StartTime
    while GPIO.input(echoAV) == 0:
        StartTime = time.time()
        if(time.time()-Tin>0.006):
            return 999

    # save time of arrival
    while GPIO.input(echoAV) == 1:
        StopTime = time.time()
        if(time.time()-Tin>0.006):
            return 999

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

if (bnoStato):
    def readGyroYaw():
        eading, roll, pitch = bno.read_euler()
        return eading
    
    
'''
def distanceID():
    # set Trigger to HIGH
    GPIO.output(triggerID, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(triggerID, False)

    StartTime = time.time()
    StopTime = time.time()
    Tin=time.time()
    # save StartTime
    while GPIO.input(echoID) == 0:
        StartTime = time.time()
        if(time.time()-Tin>0.006):
            return 999

    # save time of arrival
    while GPIO.input(echoID) == 1:
        StopTime = time.time()
        if(time.time()-Tin>0.006):
            return 999
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

'''


def distanceDX():
    # set Trigger to HIGH
    GPIO.output(triggerDX, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(triggerDX, False)

    StartTime = time.time()
    StopTime = time.time()
    Tin=time.time()


    # save StartTime
    while GPIO.input(echoDX) == 0:
        StartTime = time.time()
        if(time.time()-Tin>0.006):
                return 999


    # save time of arrival
    while GPIO.input(echoDX) == 1:
        StopTime = time.time()
        if(time.time()-Tin>0.006):
            return 999

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance


def distanceSX():
    # set Trigger to HIGH
    GPIO.output(triggerSX, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(triggerSX, False)

    StartTime = time.time()
    StopTime = time.time()
    inVal=time.time()
    # save StartTime
    while GPIO.input(echoSX) == 0:
        StartTime = time.time()
        if(time.time()-inVal>0.006):
            return 999

    # save time of arrival
    while GPIO.input(echoSX) == 1:
        StopTime = time.time()
        if(time.time()-inVal>0.006):
            return 999

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance


MDIpin=10
GPIO.setup(MDIpin, GPIO.OUT)
MDI = GPIO.PWM(MDIpin, 330)
MDI.start(0)
MDI.ChangeDutyCycle(0)

MDApin=8
GPIO.setup(MDApin, GPIO.OUT)
MDA = GPIO.PWM(MDApin, 330)
MDA.start(0)
MDA.ChangeDutyCycle(0)

BDpin=7
GPIO.setup(BDpin, GPIO.OUT)
BD = GPIO.PWM(BDpin, 50)
BD.start(0)
BD.ChangeDutyCycle(0)

PDpin=4
GPIO.setup(PDpin, GPIO.OUT)
PD = GPIO.PWM(PDpin, 50)
PD.start(0)
#PD.ChangeDutyCycle(5.5)

SCpin=17
GPIO.setup(SCpin, GPIO.OUT)
SC = GPIO.PWM(SCpin, 50)
SC.start(0)
#SC.ChangeDutyCycle(8.1)
time.sleep(0.5)
SC.ChangeDutyCycle(0)

BSpin=18
GPIO.setup(BSpin, GPIO.OUT)
BS = GPIO.PWM(BSpin, 50)
BS.start(0)
BS.ChangeDutyCycle(0)

MSApin=22
GPIO.setup(MSApin, GPIO.OUT)
MSA = GPIO.PWM(MSApin, 330)
MSA.start(0)
MSA.ChangeDutyCycle(0)

def SetupPinzaDx():
    PSpin=23
    GPIO.setup(PSpin, GPIO.OUT)
    global PS
    PS = GPIO.PWM(PSpin, 50)
    PS.start(0)
SetupPinzaDx()
#PS.ChangeDutyCycle(9.5)

MSIpin=24
GPIO.setup(MSIpin, GPIO.OUT)
MSI = GPIO.PWM(MSIpin, 330)
MSI.start(0)
MSI.ChangeDutyCycle(0)

SDpin=25
GPIO.setup(SDpin, GPIO.OUT)
SD = GPIO.PWM(SDpin, 50)
SD.start(0)
SD.ChangeDutyCycle(0)

SSpin=27
GPIO.setup(SSpin, GPIO.OUT)
SS = GPIO.PWM(SSpin, 50)
SS.start(0)
SS.ChangeDutyCycle(0)


  
#P2pin=3
#GPIO.setup(P2pin, GPIO.IN)

#P1pin=2
#GPIO.setup(P1pin, GPIO.IN)

#MSA.ChangeDutyCycle(50)
#time.sleep(20)


#MSA.ChangeDutyCycle(72)
#MSI.ChangeDutyCycle(75) #uguale vel


#MSA.ChangeDutyCycle(19)
#MSI.ChangeDutyCycle(23) #uguale vel

#MDA.ChangeDutyCycle(20)
#MDI.ChangeDutyCycle(20) #uguale vel

#MDA.ChangeDutyCycle(71)
#MDI.ChangeDutyCycle(75) #uguae vel

#time.sleep(2)

#MSA.ChangeDutyCycle(47)
#MSI.ChangeDutyCycle(47)

global statoPRE
statoPRE=0


global MuoviMot
MuoviMot=True
global mutexMot
mutexMot = 0
def SetMutex():
    global mutexMot
    mutexMot = 1
    
def ResetMutex():
    global mutexMot
    mutexMot = 0
    
def VmotoriMutex(dx,sx):
    dx=np.clip(dx,-100,100)
    sx=np.clip(sx,-100,100)

    if(dx==0):
        MDA.ChangeDutyCycle(0)
        MDI.ChangeDutyCycle(0)    
    else:
        Vdx=-int(dx*28/100)+47
        MDA.ChangeDutyCycle(Vdx)
        MDI.ChangeDutyCycle(Vdx)
    
    
    if(sx==0):
        MSA.ChangeDutyCycle(0)
        MSI.ChangeDutyCycle(0)
    else:
        Vsx=int(sx*28/100)+47
        MSA.ChangeDutyCycle(Vsx)
        MSI.ChangeDutyCycle(Vsx)


def Vmotori(dx,sx):
    #global statoPRE
    #global MuoviMot
    global mutexMot
    if(mutexMot == 1):
        return
    '''
    stato=GPIO.input(P2pin)
    #print(stato)
    if(stato==1 and statoPRE==0):
        MuoviMot=not MuoviMot
    statoPRE=stato
     
        
    
    if(MuoviMot==0):
        dx=0
        sx=0
        
    '''
    
    dx=np.clip(dx,-100,100)
    sx=np.clip(sx,-100,100)
    
    
    

    
    if(dx==0):
        MDA.ChangeDutyCycle(0)
        MDI.ChangeDutyCycle(0)    
    else:
        Vdx=-int(dx*28/100)+47
        MDA.ChangeDutyCycle(Vdx)
        MDI.ChangeDutyCycle(Vdx)
    
    
    if(sx==0):
        MSA.ChangeDutyCycle(0)
        MSI.ChangeDutyCycle(0)
    else:
        Vsx=int(sx*28/100)+47
        MSA.ChangeDutyCycle(Vsx)
        MSI.ChangeDutyCycle(Vsx)
        
def VmotoriFIX(dx,sx):
    global statoPRE
    global MuoviMot
    dx=np.clip(dx,-100,100)
    sx=np.clip(sx,-100,100)
    
    
    

    
    if(dx==0):
        MDA.ChangeDutyCycle(0)
        MDI.ChangeDutyCycle(0)    
    else:
        Vdx=-int(dx*28/100)+47
        MDA.ChangeDutyCycle(Vdx)
        Vdx=-int(dx*1.4*28/100)+47
        MDI.ChangeDutyCycle(Vdx)
    
    
    if(sx==0):
        MSA.ChangeDutyCycle(0)
        MSI.ChangeDutyCycle(0)
    else:
        Vsx=int(sx*28/100)+47
        MSA.ChangeDutyCycle(Vsx)
        MSI.ChangeDutyCycle(Vsx)

def cameraGiu():
    #piu basso e piu la camera e alta
    #SC.ChangeDutyCycle(8.0)
    for i in range(65,87,1):
        SC.ChangeDutyCycle(i/10)
        time.sleep(0.05)
        
    time.sleep(0.3)
    SC.ChangeDutyCycle(0)
    

def cameraSu():
    for i in range(86,65,-1):
        SC.ChangeDutyCycle(i/10)
        time.sleep(0.05)
    time.sleep(0.5)
    SC.ChangeDutyCycle(0)

def cameraSuRinf():
 
    SC.ChangeDutyCycle(6)
    time.sleep(0.3)
    SC.ChangeDutyCycle(0)

def cameraSuFAST():

    SC.ChangeDutyCycle(6.4)
    time.sleep(0.5)
    SC.ChangeDutyCycle(0)


def Braccio(val):
            val=val/11.235955+0.6
            #val=np.clip(val,0.6,9.5)
            val=np.clip(val,1,9.5)
            
            DX=12-val
            
            DS=2+val
            
            BS.ChangeDutyCycle(DS)
            BD.ChangeDutyCycle(DX)
            '''
            val=val/11.235955+0.6
            val=np.clip(val,0.6,9.5)
            #val=np.clip(val,1.3,9.5)
            
            DX=12-val
            
            DS=2+val
            
            BS.ChangeDutyCycle(DS)
            BD.ChangeDutyCycle(DX)
            '''
            
def BraccioBasso(val):
            val=val/11.235955+0.6
            val=np.clip(val,0.6,9.5)
            #val=np.clip(val,1.3,9.5)
            
            DX=12-val
            
            DS=2+val
            
            BS.ChangeDutyCycle(DS)
            BD.ChangeDutyCycle(DX)

def scaricoDX():
    #0=9 100=11
    #val=np.float32(val)/50.0+9
    #val=np.clip(val,9,11)
    

    
    SD.ChangeDutyCycle(6.5)
    #SS.ChangeDutyCycle(11)
    time.sleep(1.5)
    SD.ChangeDutyCycle(3.5)
    time.sleep(1)    
    #SS.ChangeDutyCycle(0)
    
    SD.ChangeDutyCycle(0)

    
def scaricoSX():

    SS.ChangeDutyCycle(8.2)
    #SD.ChangeDutyCycle(3.5)
    time.sleep(1.5)
    SS.ChangeDutyCycle(11)
    time.sleep(1.5)  
    SS.ChangeDutyCycle(0)
    #SD.ChangeDutyCycle(0)

def PinzaDX(val):
    val=val/33.333+5
    val=np.clip(val,5,7.4)
    PS.ChangeDutyCycle(val)

def PinzaSX(val):

    val=6.8-val/33.333
    val=np.clip(val,4.5,6.8)
    PD.ChangeDutyCycle(val)
    
def PinzaRelax():
    

    
    PD.ChangeDutyCycle(0)
    PS.ChangeDutyCycle(0)

    

def caricoSX():
    Vmotori(0,0)
    PinzaRelax()
    global statoPinza
    statoPinza=1
    for i in range(80,0,-1):
        Braccio(i)
        time.sleep(0.04)
        
        
    BS.ChangeDutyCycle(0)
    BD.ChangeDutyCycle(0)
    
    Vmotori(30,30)
    time.sleep(0.4)
    Vmotori(0,0)
    
    for i in range(100,0,-1):
        PinzaSX(i)
        PinzaDX(i)
        time.sleep(0.005)
    
    
    Vmotori(-30,-30)
    time.sleep(0.3)
    Vmotori(0,0)
    
    
    
    for i in range(0,80,1):
        Braccio(i)
        time.sleep(0.04)
        
    
        
    BS.ChangeDutyCycle(0)
    BD.ChangeDutyCycle(0)
    
    for i in range(0,30,1):
        PinzaSX(i)
        PinzaDX(i)
        time.sleep(0.005)
    
    for i in range(30,100,1):
        #PinzaSX(i)
        PinzaDX(i)
        time.sleep(0.005)
    
    time.sleep(0.5)
    
    for i in range(30,100,1):
        PinzaSX(i)
        #PinzaDX(i)
        time.sleep(0.005)
    
    #PinzaSX(30)
    #PinzaDX(100)
    
    time.sleep(0.5)
    
    BS.ChangeDutyCycle(0)
    BD.ChangeDutyCycle(0)
    
    
    PinzaRelax()
    
    #PinzaSX(100)
    #PinzaDX(100)
    statoPinza=0

def caricoDX():
    Vmotori(0,0)
    PinzaRelax()
    
    global statoPinza
    
    statoPinza=1
    for i in range(80,0,-1):
        Braccio(i)
        time.sleep(0.04)
    
    time.sleep(0.3)
        
    BS.ChangeDutyCycle(0)
    BD.ChangeDutyCycle(0)
    
    time.sleep(0.3)
    
    Vmotori(30,30)
    time.sleep(0.4)
    Vmotori(0,0)
    
    time.sleep(0.3)
    
    for i in range(100,0,-1):
        PinzaSX(i)
        PinzaDX(i)
        time.sleep(0.005)
    
    time.sleep(0.5)
    
    Vmotori(-30,-30)
    time.sleep(0.4)
    Vmotori(0,0)
    
    time.sleep(0.3)
    
    for i in range(0,80,1):
        Braccio(i)
        time.sleep(0.04)
        
    time.sleep(0.3)
        
    BS.ChangeDutyCycle(0)
    BD.ChangeDutyCycle(0)
    
    time.sleep(0.3)
    
    for i in range(0,30,1):
        PinzaSX(i)
        PinzaDX(i)
        time.sleep(0.005)
    
    for i in range(30,100,1):
        PinzaSX(i)
        #PinzaDX(i)
        time.sleep(0.005)
    
    time.sleep(0.5)
    
    for i in range(30,100,1):
        #PinzaSX(i)
        PinzaDX(i)
        time.sleep(0.005)
    
    #PinzaSX(30)
    #PinzaDX(100)
    
    time.sleep(0.3)

    
    PinzaRelax()
    
    #PinzaSX(100)
    #PinzaDX(100)
    statoPinza=0

    
    
def fixPinza():
    global statoPinza

    while 1:
        if(statoPinza==0):
            PinzaSX(80)
            PinzaDX(80)
            
            
        time.sleep(0.5)
            
        
        if(statoPinza==0):
            PD.ChangeDutyCycle(0)
            PS.ChangeDutyCycle(0)
            
        time.sleep(2)

  
global statoPinza
statoPinza=0
  
#FixP=Thread(target=fixPinza,args=())
#FixP.start()
    
Braccio(80)

time.sleep(0.5)

BS.ChangeDutyCycle(0)
BD.ChangeDutyCycle(0)

PinzaSX(50)

PinzaRelax()

def distanzaAngolare(x1,x2):
    distanza=x1-x2
    if(distanza>180):
        distanza-=360
        
    if(distanza<-180):
        distanza+=360
        
    return(distanza)
if (bnoStato):
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
            delta=np.clip(delta,-50,50)
            Vmotori(delta,-delta)
            if(delta>-1 and delta<1):
                break
        print('errore giro:',delta)
        Vmotori(0,0)
        
    def giraTo(val):
        angolo=val
        
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
            delta=np.clip(delta,-50,50)
            Vmotori(delta,-delta)
            if(delta>-1 and delta<1):
                break
        print('errore giro:',delta)
        Vmotori(0,0)
        

        

def BraccioGiu():
    for i in range(80,0,-1):
        Braccio(i)
        time.sleep(0.04)
        
    time.sleep(0.3)
        
    BS.ChangeDutyCycle(0)
    BD.ChangeDutyCycle(0)
    


def BraccioGiuScarico():
    for i in range(80,60,-1):
        Braccio(i)
        time.sleep(0.04)
        
    time.sleep(0.3)
        
    BS.ChangeDutyCycle(0)
    BD.ChangeDutyCycle(0)
    

def BraccioSuScarico():
    for i in range(60,80,1):
        Braccio(i)
        time.sleep(0.04)
        
    time.sleep(0.3)
        
    BS.ChangeDutyCycle(0)
    BD.ChangeDutyCycle(0)

def BraccioSu():
    for i in range(0,90,1):
        Braccio(i)
        time.sleep(0.04)
        
    time.sleep(0.3)
        
    BS.ChangeDutyCycle(0)
    BD.ChangeDutyCycle(0)

def BraccioSuCubo():
    for i in range(0,90,1):
        BraccioBasso(i)
        time.sleep(0.04)
        
    time.sleep(0.3)
        
    BS.ChangeDutyCycle(0)
    BD.ChangeDutyCycle(0)


def BraccioSuCubo2():
    for i in range(0,80,1):
        BraccioBasso(i)
        time.sleep(0.04)
        
    time.sleep(0.3)
        
    BS.ChangeDutyCycle(0)
    BD.ChangeDutyCycle(0)



def BraccioGiuCubo():
    for i in range(80,0,-1):
        BraccioBasso(i)
        time.sleep(0.04)
        
    time.sleep(0.3)
        
    BS.ChangeDutyCycle(0)
    BD.ChangeDutyCycle(0)
def BraccioImmezzoCubo():
    for i in range(90,80,-1):
        BraccioBasso(i)
        time.sleep(0.04)
        
    time.sleep(0.3)
        
    BS.ChangeDutyCycle(0)
    BD.ChangeDutyCycle(0)
    

def ControlloPinza():
    
    global PS
    
    print()
    imgPre=foto()[200:400,200:600,1]

    Cfermi=0

    

    PinzaDX(80)
    #PinzaSX(80)

    while 1:
        img=foto()[200:400,200:600,1]
        
        #pixel mossi
        imgDelta=np.int16(img)-imgPre
        
        #modulo di imgDelta
        imgDelta[imgDelta<0]*=-1
        
        #offset per evitare disturbi
        imgDelta[imgDelta<50]=0
        
        #print(np.amin(imgDelta),np.amax(imgDelta))
        
        movimento = np.sum(imgDelta)
        #print(movimento)
        if(movimento<4000):
            Cfermi+=1
        else:
            Cfermi=0
        #print(Cfermi)
        if(Cfermi==0):
            PinzaDX(80)
        
        if(Cfermi>10):
            PD.ChangeDutyCycle(0)

            
        if(Cfermi>20):
            #print('fine')
            break
        time.sleep(0.05)
            
        imgPre=img.copy()
    
    #PinzaDX(80)
    PinzaSX(80)

    while 1:
        img=foto()[200:400,200:600,1]
        
        #pixel mossi
        imgDelta=np.int16(img)-imgPre
        
        #modulo di imgDelta
        imgDelta[imgDelta<0]*=-1
        
        #offset per evitare disturbi
        imgDelta[imgDelta<50]=0
        
        #print(np.amin(imgDelta),np.amax(imgDelta))
        
        movimento = np.sum(imgDelta)
        #print(movimento)
        if(movimento<4000):
            Cfermi+=1
        else:
            Cfermi=0
        #print(Cfermi)
        if(Cfermi==0):
            PinzaSX(80)
        
        if(Cfermi>10):
            PS.ChangeDutyCycle(0)

            
        if(Cfermi>30):
            #print('fine')
            break
        time.sleep(0.05)
            
        imgPre=img.copy()
        
    

def readP3():
   return GPIO.input(P3pin) 


if __name__ == '__main__':
    
    
    
    while 1:
        print(distanceAV())
        time.sleep(0.1)
    
    print('ok')
    time.sleep(3)
    scaricoDX()
    
    
    #cameraSu()
    time.sleep(1000)

    Braccio(80)

    #SD.ChangeDutyCycle(5.5)
    #SS.ChangeDutyCycle(9)
    
    #PinzaDX(80)
    #PinzaSX(80)
    
    #SD.ChangeDutyCycle(3.5)
    #SS.ChangeDutyCycle(11)
    #avvioStreamHD()
    print('ok')
    time.sleep(10000)
    
    while 0:
        PinzaDX(30)
        PinzaSX(30)
        time.sleep(np.random.random_sample())
        PD.ChangeDutyCycle(0)
        PS.ChangeDutyCycle(0)
        time.sleep(0.5)
        
    
    
    time.sleep(3)
    while 1:
        playSound()
    #scaricoDX()
    #scaricoSX()
    #PinzaDX(0)
    #PinzaSX(0)
    time.sleep(300000000)
    ControlloPinza()

    '''
    giraDi(180)
    giraDi(90)
    giraDi(45)
    giraDi(30)
    giraDi(15)
    
    print('aa')
    Vmotori(30,30)
    #MDA.ChangeDutyCycle(50)
    #MDI.ChangeDutyCycle(50)
    time.sleep(10000)
    print(111)
    print(distanceAV())
    while 1:
        print(distanceDX())
    #scaricoSX()
    
    #SS.ChangeDutyCycle(2.5)
    #time.sleep(0.4)
    
    #APERTA
    #PD.ChangeDutyCycle(6)
    
    #PS.ChangeDutyCycle(8)
    
    #scaricoSX()
    #PinzaSX(30)
    #PinzaDX(100)
    #caricoDX()
    time.sleep(111)
    

    '''
    '''
    #Vmotori(20,20)

    while 1:
        cameraGiu()
        time.sleep(0.5)
        cameraSu()
        time.sleep(0.5)
    a=0
    
    for i in range(100,0,-1):
        Braccio(i)
        time.sleep(0.04)
    for i in range(100):
        Braccio(i)
        time.sleep(0.04)
    Vmotori(0,0)
    #cameraGiu()
    
    #BS.ChangeDutyCycle(2.2)
    #BD.ChangeDutyCycle(12)
    '''
    
    '''
    
    while 1:
        for i in range(0,100):
            val=i/10
        
            val=np.clip(val,0.6,10)
            
            DX=12-val
            
            DS=2+val
            
            BS.ChangeDutyCycle(DS)
            BD.ChangeDutyCycle(DX)
            
            time.sleep(0.04)
            
        for i in range(100,0,-1):
            val=i/10
        
            val=np.clip(val,0.6,10)
            
            DX=12-val
            
            DS=2+val
            
            BS.ChangeDutyCycle(DS)
            BD.ChangeDutyCycle(DX)
            
            time.sleep(0.04)
    '''
    #Vmotori(-50,50)
    #time.sleep(100)
    #Vmotori(0,0)

    #while 1:
        #dist = distanceSX()
        #print(dist)
        #print(GPIO.input(P2pin),GPIO.input(P1pin))
        #time.sleep(0.1)

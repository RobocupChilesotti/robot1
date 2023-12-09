import cv2
import numpy as np
import multiprocessing
from robot import Vmotori
from cattura import foto
from Semplifica import semplifica
from cattura import avvioStream128
from cattura import avvioStreamHD
from cattura import stopStream
from robot import cameraSu
from robot import cameraGiu
from robot import distanceAV
from robot import distanceDX
from robot import distanceSX
from threading import Thread
from detector3 import palline
#from detector4 import palline
from robot import scaricoDX
from robot import scaricoSX
#from robot import RaccoltaPallina
from robot import ControlloPinza
from robot import BraccioSu
from robot import BraccioGiu
from robot import PinzaSX as PinzaDX
from robot import PinzaDX as PinzaSX
#from robot import palline
from robot import cameraSuRinf
from robot import VmotoriMutex
from robot import ResetMutex
from robot import SetMutex
from robot import readP3
from robot import PinzaRelax
from robot import BraccioImmezzoCubo
import time
import variabili
from robot import BraccioSuScarico
from robot import BraccioGiuScarico

#setup
global PosOstacolo
#PosOstacolo = 'centro'
PosOstacolo = 'lato'




#Vmotori(20,20)
#time.sleep(1000)

#cameraSu()
#avvioStreamHD()

sigma=10

#luce normale
lower_red = np.array([0,70,90])
upper_red = np.array([20,255,240])
                      #B  G   R     
                      #H  S   V  
lower_red2 = np.array([130,70,90])
upper_red2 = np.array([255,255,240])

#luce buio
#lower_red = np.array([0,70,40])
#upper_red = np.array([20,255,240])
                      #B  G   R     
                      #H  S   V  
#lower_red2 = np.array([130,70,40])
#upper_red2 = np.array([255,255,240])

#no luce rossa
lower_green = np.array([30,120,55]) 
upper_green = np.array([95,255,205])

lower_green_vic = np.array([30,55,60]) 
upper_green_vic = np.array([70,255,200])

lower_green_vic = lower_green
upper_green_vic = upper_green_vic

#luce rossa
#lower_green = np.array([70,10,60]) 
#upper_green = np.array([130,255,110])

lower_gray = np.array([0,0,100]) 
upper_gray = np.array([255,255,200])

def dx90():
    Vmotori(-30,30)
    time.sleep(2.3)
    Vmotori(0,0)
    return

def sx90():
    Vmotori(30,-30)
    time.sleep(2)
    Vmotori(0,0)
    return

def dxT(T):
    Vmotori(-30,30)
    time.sleep(T)
    Vmotori(0,0)
    return
def sxT(T):
    Vmotori(30,-30)
    time.sleep(T)
    Vmotori(0,0)
    return

def dx30():
    Vmotori(-30,30)
    time.sleep(0.7)
    Vmotori(0,0)
    return


def sx30():
    Vmotori(30,-30)
    time.sleep(0.7)
    Vmotori(0,0)
    return

def dxT(T):
    Vmotori(-30,30)
    time.sleep(T)
    Vmotori(0,0)
    return


def sxT(T):
    Vmotori(30,-30)
    time.sleep(T)
    Vmotori(0,0)
    return

def sx15():
    Vmotori(30,-30)
    time.sleep(0.5)
    Vmotori(0,0)
    return

def dx15():
    Vmotori(-30,30)
    time.sleep(0.5)
    Vmotori(0,0)
    return

def Distanza2punti(p1y,p1x,p2y,p2x):
    return ((p1x-p2x)**2+(p1y-p2y)**2)**0.5


def undesired_objects (image):
    image = image.astype('uint8')
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(image, connectivity=4)
    sizes = stats[:, -1]
    #if(np.shape(max_size))
    if(np.shape(sizes)[0]==1):
        return image
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
    


def ObjectDetector():
    global StatoDetector
    StatoDetector=0

    global bianca
    bianca = (0,0)
    
    global nera
    nera = (0,0)
    
    global ostacolo
    ostacolo = (0,0)
    
    global update
    update=0
    
    global imgDetector
    imgDetector=foto()
    
    while 1:
        while StatoDetector:
            imgDetector,bianca,nera,ostacolo=palline()
            #print('running')
            update=1
        while (StatoDetector==0):
            time.sleep(0.05)


Thread(target=ObjectDetector,args=()).start()


def DXred():


    global bianca
    global nera
    
    
    
    kernel = np.ones((5,5),np.uint8)
    kernel2 = np.ones((25,25),np.uint8)
    imgB=np.zeros((600,800),dtype=np.uint8)


    
        
    while 1:
        Vmotori(-30,30)
        img=foto()
        
        
        if(bianca != (0,0) or nera != (0,0) or (ostacolo!=(0,0) and ostacolo[0]> 250 and ostacolo[1]>100 and  ostacolo[1]<700)):
            break
        
        gray = cv2.cvtColor(img[200:300,:], cv2.COLOR_BGR2GRAY)
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

        area = cv2.morphologyEx(area, cv2.MORPH_CLOSE, kernel2)

        imgMezzi=img[200:300,:]
        
        imgMezzi[area==255,1]=255
        
        img[200:300,:]=imgMezzi
        
        img=cv2.rectangle(img,(600,200),(785,300),(0,0,255),thickness=1)
        #img=cv2.rectangle(img,(15,200),(100,400),(0,0,255),thickness=1)
        
        img=cv2.rectangle(img,(200,200),(600,300),(255,0,0),thickness=1)
        

        
        #print(np.count_nonzero(255-area))
        
        if(np.count_nonzero(255-area)<10000):
            #print('break')
            break
        


        cv2.imshow('img',img)
        cv2.waitKey(1)&0xff
        
    Vmotori(0,0)

def DXred2():
    
    global bianca
    global nera

    
    kernel = np.ones((5,5),np.uint8)
    kernel2 = np.ones((25,25),np.uint8)
    imgB=np.zeros((600,800),dtype=np.uint8)


    
        
    while 1:
        Vmotori(-30,30)
        img=foto()
        
        
        if(bianca != (0,0) or nera != (0,0) or (ostacolo!=(0,0) and ostacolo[0]> 250 and ostacolo[1]>100 and  ostacolo[1]<700)):
            break
            
        gray = cv2.cvtColor(img[200:300,:], cv2.COLOR_BGR2GRAY)
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

        area = cv2.morphologyEx(area, cv2.MORPH_CLOSE, kernel2)

        imgMezzi=img[200:300,:]
        
        imgMezzi[area==255,1]=255
        
        img[200:300,:]=imgMezzi
        
        img=cv2.rectangle(img,(600,200),(785,300),(0,0,255),thickness=1)
        #img=cv2.rectangle(img,(15,200),(100,400),(0,0,255),thickness=1)
        
        img=cv2.rectangle(img,(200,200),(600,300),(255,0,0),thickness=1)
        

        
        #print(np.count_nonzero(255-area))
        
        if(np.count_nonzero(255-area[:,100:400])<10000):
            #print('break')
            break
        


        cv2.imshow('img',img)
        cv2.waitKey(1)&0xff
        
    Vmotori(0,0)

def SXred():

    global bianca
    global nera
    global ostacolo

    
    kernel = np.ones((5,5),np.uint8)
    kernel2 = np.ones((25,25),np.uint8)
    imgB=np.zeros((600,800),dtype=np.uint8)


    while 1:
        Vmotori(30,-30)
        img=foto()
        
        
        if(bianca != (0,0) or nera != (0,0) or (ostacolo!=(0,0) and ostacolo[0]> 250 and ostacolo[1]>100 and  ostacolo[1]<700)):
                
             
            break
            
        gray = cv2.cvtColor(img[200:300,:], cv2.COLOR_BGR2GRAY)
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

        area = cv2.morphologyEx(area, cv2.MORPH_CLOSE, kernel2)

        imgMezzi=img[200:300,:]
        
        imgMezzi[area==255,1]=255
        
        img[200:300,:]=imgMezzi
        
        img=cv2.rectangle(img,(600,200),(785,300),(0,0,255),thickness=1)
        #img=cv2.rectangle(img,(15,200),(100,400),(0,0,255),thickness=1)
        
        img=cv2.rectangle(img,(200,200),(600,300),(255,0,0),thickness=1)
        

        
        #print(np.count_nonzero(255-area))
        
        if(np.count_nonzero(255-area)<10000):
            #print('break')
            break
        


        cv2.imshow('img',img)
        cv2.waitKey(1)&0xff
        
    Vmotori(0,0)


def SXred2():
    
    
    global bianca
    global nera
    
    kernel = np.ones((5,5),np.uint8)
    kernel2 = np.ones((25,25),np.uint8)
    imgB=np.zeros((600,800),dtype=np.uint8)


    while 1:
        Vmotori(30,-30)
        img=foto()
            
            
            
        if(bianca != (0,0) or nera != (0,0) or (ostacolo!=(0,0) and ostacolo[0]> 250 and ostacolo[1]>100 and  ostacolo[1]<700)):
            break
            
        gray = cv2.cvtColor(img[200:300,:], cv2.COLOR_BGR2GRAY)
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

        area = cv2.morphologyEx(area, cv2.MORPH_CLOSE, kernel2)

        imgMezzi=img[200:300,:]
        
        imgMezzi[area==255,1]=255
        
        img[200:300,:]=imgMezzi
        
        img=cv2.rectangle(img,(600,200),(785,300),(0,0,255),thickness=1)
        #img=cv2.rectangle(img,(15,200),(100,400),(0,0,255),thickness=1)
        
        img=cv2.rectangle(img,(200,200),(600,300),(255,0,0),thickness=1)
        

        
        #print(np.count_nonzero(255-area))
        
        if(np.count_nonzero(255-area[:,400:700])<10000):
            #print('break')
            break
        


        cv2.imshow('img',img)
        cv2.waitKey(1)&0xff
        
    Vmotori(0,0)
def AllineamentoOstacolo(tipo):
    Cpersi=0
    Cvicini=0
    
    
    stato = 0 # 0 AVANTI 1 INDIETRO
    
    while 1:
        imgDetector,bianca,nera,ostacolo=palline()
        
        if (tipo == 'bianca'):
            pos = bianca
        else:
            pos = nera
        
        if(pos!= (0,0) and ostacolo!= (0,0)):
            Cpersi = 0
            
            Xmin = min((pos[1],ostacolo[1]))
            Xmax = max((pos[1],ostacolo[1]))
            DeltaX = pos[1]-ostacolo[1] # se DeltaX < 0 allora l'ostacolo e a destra
            
            if(DeltaX <25 and DeltaX >-25):
                print('pallina e ostacolo accentrati')
                if(pos[0]>300):
                    Vmotori(30,30)
                    time.sleep(0.4)
                RaccoltaPallina(tipo + 'O')
                break
            
            Ymax = max((pos[0]),ostacolo[0])
            
            print(DeltaX)
            
            if(Ymax>380 and stato==0):
                stato =1
                if(DeltaX >200 or DeltaX <-200):
                    if(DeltaX<0):
                        Vmotori(-30,-30)
                        time.sleep(0.5)
                        Vmotori(-35,35)
                        time.sleep(3)
                        Vmotori(-30,-30)
                        time.sleep(3)
                        Vmotori(0,0)
                        Vmotori(30,-30)
                        time.sleep(1.4)
                    else:
                        Vmotori(-30,-30)
                        time.sleep(0.5)
                        Vmotori(35,-35)
                        time.sleep(3)
                        Vmotori(-30,-30)
                        time.sleep(3)
                        Vmotori(-30,30)
                        time.sleep(1.4)
                        Vmotori(0,0)
                        
                
                    
            if(Ymax<250):
                stato =0
                

            
            
            #print(stato,DeltaX)
            
            
            if(stato == 0):
                #avanti
                if(DeltaX<0):
                    #ostacolo a destra della pallina
                    deltaX = 600-Xmax
                    deltaY = 400-Ymax
                else:
                    #ostacolo a sinistra della pallina
                    deltaX = 200-Xmin
                    deltaY = 400-Ymax
                    
                if(deltaY>100):
                    deltaX/=2
                    
            else:
                #indietro
                if(DeltaX<0):
                    #ostacolo a destra della pallina
                    deltaX = 100-Xmin
                    deltaY = 220-Ymax
                else:
                    #ostacolo a sinistra della pallina
                    deltaX = 700-Xmax
                    deltaY = 220-Ymax
            
            
            if(deltaX<60 and deltaX>-60):
                Vsx = deltaY*0.4+deltaX*0.25
                Vdx = deltaY*0.4-deltaX*0.25
                
                Vmax = max(Vsx,Vsx)
                
                if(Vmax>30):
                    Vsx = Vsx/Vmax*30
                    Vdx = Vdx/Vmax*30
            else:
                Vsx = deltaY*0+deltaX*0.25
                Vdx = deltaY*0-deltaX*0.25
                
            
                Vmax = max(Vsx,Vsx)
                
                if(Vmax>20):
                    Vsx = Vsx/Vmax*20
                    Vdx = Vdx/Vmax*20
            
            Vmotori(Vsx,Vdx)
            
            
            
        else:
            Vmotori(0,0)
            Cpersi+=1
            if(Cpersi>30):
                print('persi di vista o pallina o ostacolo')
                return 0
        cv2.imshow('img',imgDetector)
        cv2.waitKey(1)&0xff

    
def RaccoltaPallina(tipo):
    
    Cpersi=0
    Cvicini=0
    
    global giro
    
    
    while 1:
        TinFPS = time.time()
        img,bianca,nera,ostacolo=palline()
        if(tipo=='nera'):
            coordinate = nera
        else:
            coordinate = bianca
        
        if(coordinate != (0,0)):
            Cpersi=0
        
            ErroreY = 200-coordinate[0]
            ErroreX = 400-coordinate[1]
            
            Vsx=ErroreY*0.4+ErroreX*0.5
            Vdx=ErroreY*0.4-ErroreX*0.5            
            Vsx=np.clip(Vsx,-20,20)
            Vdx=np.clip(Vdx,-20,20)
            
            
            Vmotori(Vsx,Vdx)
            
            deltaXo = ostacolo[1]-coordinate[1]
            deltaYo = ostacolo[0]-coordinate[0]
            
            if(deltaXo<0):
                deltaXo=-deltaXo
            
            #print(deltaYo,deltaXo)
            
            #deltaYo += 25 - deltaXo/2
            #ostacolo troppo vicino alla pallina, creo allineamento
            if(deltaYo > 20 and deltaXo<230 and coordinate[0] > 180):
                AllineamentoOstacolo(tipo)            


            
            if(ErroreY<30 and ErroreY>-30 and ErroreX<30 and ErroreX>-30):
                Cvicini+=1
                
                if(Cvicini>10):
                    break
                
            else:
                Cvicini=0
            
            
        else:
            Cpersi+=1
            print('persa1',nera,bianca)
            if(Cpersi>10):
                Vmotori(0,0)
                print('pallina persa',nera,bianca)
                #cv2.imshow('persa',img)
                #cv2.waitKey(0)
                
                return 0
        TinFPS = time.time()
        print('fps_fase2:',1/(time.time()-TinFPS))
    Vmotori(0,0)
    #sono vicino alla palla in maniera non precisa
    
    
    print('finita fase 1, abbasso la pinza')
    #abbasso la pinza
    BraccioGiu()
    cameraSuRinf()
    #metto i becchi bene
    #ControlloPinza()
    PinzaRelax()
    
    #secondo ciclo in cui prendo la pallina
    Cpersi=0
    Cvicini=0
    CneraImmezzo=0
    
    Cfermi = 0
    
    Tin = time.time()
    coordinatePre = (0,0)
    
    while 1:
        img,bianca,nera,ostacolo=palline()
        if(tipo=='bianca'):
            coordinate = bianca
        else:
            coordinate = nera
        if(coordinate != (0,0)):
            Cpersi=0
            if(tipo=='bianca'):

                ErroreY = 270-coordinate[0]
                
                ErroreXn=430-nera[1]
                ErroreYn=300-nera[0]
                
                if(ErroreYn<25 and ErroreYn>-25 and ErroreXn<25 and ErroreXn>-25):
                    CneraImmezzo+=1
                    if(CneraImmezzo>10):
                        
                        spostaPallinaNera(1)
                        
                        
                else:
                    CneraImmezzo=0
                
            else:
                #settaggioScuola
                #ErroreY = 285-coordinate[0]
                
                #settaggioCasa
                ErroreY = 270-coordinate[0]
     
                
            ErroreX = 420-coordinate[1]
            
            
            
            Vsx=ErroreY*0.5+ErroreX*0.5
            Vdx=ErroreY*0.5-ErroreX*0.5
            
            Vsx=np.clip(Vsx,-20,20)
            Vdx=np.clip(Vdx,-20,20)
            
            
            Vmotori(Vsx,Vdx)
            
            deltaX = coordinate[1]-coordinatePre[1]
            deltaY = coordinate[0]-coordinatePre[0]
            
            
            if(ErroreY<10 + time.time()-Tin and ErroreY>-15 and ErroreX<15 and ErroreX>-15):
                Cvicini+=1
                
                if(Cvicini>10):
                    break
                
            else:
                Cvicini=0
                
            if(deltaX<4 and deltaX>-4 and deltaY<4 and deltaY>-4):
                Cfermi+=1
                
                if(Cfermi>10):
                    break
                
            else:
                Cfermi=0
            
            
        else:
            Cpersi+=1
            
            if(Cpersi>10):
                Vmotori(0,0)
                print('persa pallina, ritiro la pinza')
                BraccioSu()
                BraccioImmezzoCubo()
                return 0
        
        
        coordinatePre = coordinate
        cv2.imshow('img',img)
        cv2.waitKey(1)&0xff
    

    Vmotori(20,20)
    time.sleep(0.5)

    
    Vmotori(0,0)
    time.sleep(0.3)
    
    for i in range(80,0,-1):
        PinzaSX(i)
        PinzaDX(i)
        time.sleep(0.005)
    
    time.sleep(0.3)
    
    Vmotori(-20,-20)
    time.sleep(0.3)
    Vmotori(0,0)
    time.sleep(0.3)
    BraccioSu()
    
    
    time.sleep(0.3)
    
    
    for i in range(0,30,1):
        PinzaSX(i)
        PinzaDX(i)
        time.sleep(0.005)
        
    if(tipo=='bianca'):
        
        global raccoltaBianca
        raccoltaBianca +=1

        
        for i in range(30,100,1):
            PinzaSX(i)
            #PinzaDX(i)
            time.sleep(0.005)
        
        time.sleep(1)
        
        for i in range(30,100,1):
            #PinzaSX(i)
            PinzaDX(i)
            time.sleep(0.005)
    else:
        global raccoltaNera
        raccoltaNera +=1

        
        for i in range(30,100,1):
            PinzaDX(i)
            #PinzaDX(i)
            time.sleep(0.005)
        
        time.sleep(1)
        
        for i in range(30,100,1):
            #PinzaSX(i)
            PinzaSX(i)
            time.sleep(0.005)
    
    time.sleep(1)
    #BraccioGiu()
    #cameraSuRinf()
    #ControlloPinza()
    #BraccioSu()
    PinzaRelax()
    BraccioImmezzoCubo()
    


def greenDetectMP(queue):
    img = queue.get()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #print('hello from process',np.shape(img))
    green = cv2.inRange(hsv, lower_green, upper_green)
    img = queue.put(green)


def greenDetectMT():
    global imgMT
    global hsvTH
    hsvTH = cv2.cvtColor(imgMT, cv2.COLOR_BGR2HSV)
    #print('hello from process',np.shape(img))
    imgMT = cv2.inRange(hsvTH, lower_green, upper_green)


def esci():
    print('esco dalla pista')
    

    
    global StatoDetector
    StatoDetector=0
    
    MoltVel=1.5

    Cvicini=0

    global giro
    giro = 0
    

    p3Pre = readP3()
    


    print('in while')

    while 1:
        
        tin = time.time()
        
        p3 = readP3()
        if(p3==1 and p3Pre==0):
            Vmotori(0,0)
            giro = 1
            
            raccoltaBianca=0
            raccoltaNera = 0
            
            print('lack of progress')
            while (readP3()):
                time.sleep(0.01)
            
            while (not readP3()):
                time.sleep(0.01)
                
            while (readP3()):
                time.sleep(0.01)
                
            cameraSuRinf()
            cameraSuRinf()
                
            time.sleep(1)
            
        
        img = foto()
    
        
        hsv = cv2.cvtColor(img[:,:], cv2.COLOR_BGR2HSV)
        #print('hello from process',np.shape(img))
        green = cv2.inRange(hsv, lower_green, upper_green)
        
        
        green = undesired_objects(green)
        #print(np.shape(green))
        
        #imgMezzi[green==255,1]=255
        
        M = cv2.moments(green[50:,50:-50])
        cX = 0
        cY = 0
        if(M["m00"]!=0):
            cX = int(M["m10"] / M["m00"])-400
            cY = int(M["m01"] / M["m00"])-300
            
            
            distanza = (cX**2 + cY**2)**0.5
            if(distanza<30):
                Cvicini+=1
            
            else:
                Cvicini = 0
        
        print(cX,cY)
        
        if(Cvicini > 30):
            Vmotori(30,30)
            time.sleep(1.6)
            Vmotori(0,0)
            cv2.destroyAllWindows()
            print('torno rescue line')
            stopStream()
            cameraGiu()
            avvioStream128()
            return
            
        if(cX>40 or cX<-40):
            cY=0
        
        
        
        cY = np.clip(cY//2,-40,40)
        cX = np.clip(cX//2,-40,40)
        
        Vmotori(-cY-cX,-cY+cX)
        
        
        
        imgMezzi=img[:,:]
        
        #print(np.shape(imgMezzi),np.shape(green))
        
        imgMezzi[green==255,1]=255
        img[:,:]=imgMezzi
        
        
        

        
  
        
        cv2.imshow('img',img[150:,:,:])
        cv2.imshow('hsv',hsv)
        #cv2.imshow('maskDX',maskDX)
        cv2.waitKey(1)&0xff
        #cv2.waitKey(0)
        #scv2.waitKey(1)&0xff
        
        print('fps:',1/(time.time()-tin))

def trovaUschita():
    
    
    
    print('inizio ricerca uscita')
    
    global StatoDetector
    StatoDetector=0
    
    MoltVel=1.5



    global giro
    giro = 1
    
    Vmotori(30,30)
    time.sleep(1)
    
    if(giro == 1):
        dx90()
    else:
        sx90()
    
    
    
    #multitreading o multiprocessing
    global imgMT
    global hsvTH
    #queue = multiprocessing.Queue()
    
    

    p3Pre = readP3()
    
    
    kernel = np.ones((5,5),np.uint8)
    kernel2 = np.ones((25,25),np.uint8)
    imgB=np.zeros((600,800),dtype=np.uint8)

    print('in while')
    
    Tscarico = time.time()
    
    while 1:
        
        tin = time.time()
        
        p3 = readP3()
        if(p3==1 and p3Pre==0):
            Vmotori(0,0)
            giro = 1
            
            raccoltaBianca=0
            raccoltaNera = 0
            
            print('lack of progress')
            while (readP3()):
                time.sleep(0.01)
            
            while (not readP3()):
                time.sleep(0.01)
                
            while (readP3()):
                time.sleep(0.01)
                
            cameraSuRinf()
            cameraSuRinf()
                
            time.sleep(1)
            
        
        img = foto()
        
        imgMT = img[150:250,:]
        #queue.put(img[150:250,:])
        #p = multiprocessing.Process(target=greenDetectMP, args=(queue,))
        p = Thread(target=greenDetectMT, args=())
        p.start()
        
  
        
        gray = cv2.cvtColor(img[200:300,:], cv2.COLOR_BGR2GRAY)
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

        

        area = cv2.morphologyEx(area, cv2.MORPH_CLOSE, kernel2)

        imgMezzi=img[200:300,:]
        
        imgMezzi[area==255,0]=255
        #print('pre queue.get')
        
        img[200:300,:]=imgMezzi
        #green = queue.get()
        p.join()
        green = imgMT.copy()
        
        #print(np.shape(green))
        
        #imgMezzi[green==255,1]=255
        
        
        imgMezzi=img[150:250,:]
        
        #print(np.shape(imgMezzi),np.shape(green))
        
        imgMezzi[green==255,1]=255
        img[150:250,:]=imgMezzi
        
        
        
        
        img=cv2.rectangle(img,(15,200),(200,300),(0,0,255),thickness=1)
        img=cv2.rectangle(img,(600,200),(785,300),(0,0,255),thickness=1)
        #img=cv2.rectangle(img,(15,200),(100,400),(0,0,255),thickness=1)
        img=cv2.rectangle(img,(200,200),(600,300),(255,0,0),thickness=1)
        
  
        
        cv2.imshow('img',img[150:300,:,:])
        cv2.imshow('hsv',hsvTH)
        #cv2.imshow('hsv',hsv)
        #cv2.imshow('maskDX',maskDX)
        cv2.waitKey(1)&0xff
        #cv2.waitKey(0)
        #scv2.waitKey(1)&0xff
        

        if(time.time()-Tscarico>0.5):
            NgreenUP = np.count_nonzero(green[:,300:500])
            if(giro == 1):
                NgreenDX=np.count_nonzero(green[:,600:770])
                if(NgreenDX>1000):
                    print('vista uscita')
                    #SXred()
                    sx15()
                    Vmotori(40,40)
                    time.sleep(2.4)
                    dx30()
                    dx15()
                    esci()
                    return
                    
            else:
                NgreenSX=np.count_nonzero(green[:,30:200])
                if(NgreenSX>1000):
                    print('vista uscita')
                    #DXred()
                    dx15()
                    Vmotori(40,40)
                    time.sleep(2.4)
                    sx30()
                    sx15()
                    esci()
                    return
            
            if(NgreenUP>1000):
                print('vista uscita')
                Vmotori(20,20)
                time.sleep(0.5)
                esci()
                return
            
        
        
        sogliaH=area[:,200:600]
        NareaH=(40000-np.count_nonzero(sogliaH))/93
        
        
        if(giro == 1):
            sogliaDX=area[:,600:785]
            NareaDX=(9000-np.count_nonzero(sogliaDX))/100/6
            
            
            
            if(NareaH>80):
                Vmotori(30,30)
                time.sleep(0.5)
                sx30()
                sx15()
                SXred2()
                #sx15()
            
            Vmotori((30+NareaDX)*MoltVel,(30-NareaDX)*MoltVel)
            
            
        else:
            sogliaSX=area[:,15:200]
            NareaSX=(9000-np.count_nonzero(sogliaSX))/100/6
            
            #print(NareaH)
            
            if(NareaH>80):
                Vmotori(30,30)
                time.sleep(0.5)
                dx30()
                dx15()
                DXred2()
                #dx15()
            
            Vmotori((30-NareaSX)*MoltVel,(30+NareaSX)*MoltVel)
        
        
        print('fps:',1/(time.time()-tin))


def scaricaPalline():
    global StatoDetector
    StatoDetector=0

    global giro
    
    if(giro == 1):
        dx90()
    else:
        sx90()
        
    Cvicini = 0
    
    LastBasketVicino = time.time()-100
    
    while 1:
        
        
        img = foto()
        
        gray = cv2.cvtColor(img[100:,:], cv2.COLOR_BGR2GRAY)
        ret ,areaBasket = cv2.threshold(gray,100,255,cv2.THRESH_BINARY_INV)


        

        #asdf
            
        NumPixelBasket = np.count_nonzero(areaBasket[:,150:-150])
        print('num black pixels:',NumPixelBasket)
        
        
        if(NumPixelBasket>90000 and time.time()-LastBasketVicino>10):
            LastBasketVicino = time.time()
                
        
        if(NumPixelBasket<75000):
            areaBasket[:,:150] = 0
            areaBasket[:,-150:] = 0
            
        cv2.imshow('img',areaBasket)
        cv2.waitKey(1)&0xff
            
        M = cv2.moments(areaBasket)
        if(M["m00"]!=0):
            cX = int(M["m10"] / M["m00"])-400
            cY = int(M["m01"] / M["m00"])-170
        
        if(NumPixelBasket>75000 and time.time()-LastBasketVicino<10 and time.time()-LastBasketVicino>2 ):
            if(cX < -14):
                
                
                
                Vmotori(-30,-30)
                time.sleep(0.5)
                dxT(2)
                Vmotori(-30,-30)
                time.sleep(1)
                sxT(1)
                LastBasketVicino = time.time()-1000
        
        
        distanza = (cX**2 + cY**2)**0.5
        if(distanza<20 and NumPixelBasket>75000):
            Cvicini+=1
        else:
            Cvicini = 0
        
        if(Cvicini > 30):
            print('trovato basket: scarico palline')
            
            Vmotori(30,30)
            time.sleep(2)
            Vmotori(-30,30)
            time.sleep(6)
            Vmotori(-30,-30)
            time.sleep(2)
            Vmotori(-30,0)
            time.sleep(1)
            Vmotori(0,-30)
            time.sleep(1)
            
            Vmotori(0,0)
            BraccioGiuScarico()
            scaricoSX()
            scaricoDX()
            BraccioSuScarico()
            trovaUschita()
            return
            
            
        if(cX>40 or cX<-40):
            cY=0
        
        
        
        cY = np.clip(cY//2,-40,40)
        cX = np.clip(cX//2,-40,40)
        if(NumPixelBasket>90000):
            cX *=2
            
            
        
        Vmotori(-cY-cX,-cY+cX)
        
        
        
    
def stanza():
    global LastOstacolo
    LastOstacolo = time.time() - 30
    global PosOstacolo
    
    faseLastBasket = 0
    #stato altri thread
    global StatoDetector
    StatoDetector=1
    
    MoltVel=1.5



    global giro
    giro = 1
    

    #dati object detector
    global ostacolo
    ostacolo = (0,0)
    global bianca
    bianca = (0,0)
    global nera
    nera = (0,0)
    global update
    update=0
    global imgDetector
    imgDetector=foto()


    #memoria palline
    global raccoltaBianca
    raccoltaBianca= 0
    global raccoltaNera
    raccoltaNera = 0

    
    

    p3Pre = readP3()
    
    
    kernel = np.ones((5,5),np.uint8)
    kernel2 = np.ones((25,25),np.uint8)
    imgB=np.zeros((600,800),dtype=np.uint8)

    while 1:
        p3 = readP3()
        if(p3==1 and p3Pre==0):
            Vmotori(0,0)
            giro = 1
            
            raccoltaBianca=0
            raccoltaNera = 0
            
            print('lack of progress')
            while (readP3()):
                time.sleep(0.01)
            
            while (not readP3()):
                time.sleep(0.01)
                
            while (readP3()):
                time.sleep(0.01)
                
            cameraSuRinf()
            cameraSuRinf()
                
            time.sleep(1)
        
        
        #aspetto che i dati dell object detector siano aggiorati
        while (update==0):
            time.sleep(0.001)
        update = 0

        
        img=foto()
        

        if(raccoltaBianca>=2 and raccoltaNera>=1):
            
            #print('cerco basket')
            
            if(giro == 1):
                areaBasket = cv2.cvtColor(img[100:300,600:785], cv2.COLOR_BGR2GRAY)
            else: 
                areaBasket = cv2.cvtColor(img[100:300,15:200], cv2.COLOR_BGR2GRAY)
                
            ret ,areaBasket = cv2.threshold(areaBasket,27,255,cv2.THRESH_BINARY_INV)
            
            cv2.imshow('areaBasket',areaBasket)
            cv2.waitKey(1)&0xff
            
            NareaBasket = np.count_nonzero(areaBasket)
            
            #print(NareaBasket)
            
            if(NareaBasket>15000):
                
                faseLastBasket = 1
            
            else:
                if(faseLastBasket == 1):
                    scaricaPalline()
                    return
        '''
        if(raccoltaBianca>=2 and raccoltaNera>=1 and time.time()-lastBasket>2.5 and faseLastBasket == 1):
            scaricaPalline()
            return
        '''
            
        
        
        gray = cv2.cvtColor(img[200:300,:], cv2.COLOR_BGR2GRAY)
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

        

        area = cv2.morphologyEx(area, cv2.MORPH_CLOSE, kernel2)

        imgMezzi=img[200:300,:]
        
        imgMezzi[area==255,1]=255
        
        img[200:300,:]=imgMezzi
        
        
        img=cv2.rectangle(img,(15,200),(200,300),(0,0,255),thickness=1)
        img=cv2.rectangle(img,(600,200),(785,300),(0,0,255),thickness=1)
        #img=cv2.rectangle(img,(15,200),(100,400),(0,0,255),thickness=1)
        img=cv2.rectangle(img,(200,200),(600,300),(255,0,0),thickness=1)
        
        
        cv2.imshow('img',img)
        #cv2.imshow('hsv',hsv)
        #cv2.imshow('maskDX',maskDX)
        cv2.waitKey(1)&0xff
        
        
        sogliaH=area[:,200:600]
        NareaH=(40000-np.count_nonzero(sogliaH))/93
        
        
        if(giro == 1):
            sogliaDX=area[:,600:785]
            NareaDX=(9000-np.count_nonzero(sogliaDX))/100/6
            
            
            if(NareaH>80):
                SXred2()
                sx15()

            Vmotori((30+NareaDX)*MoltVel,(30-NareaDX)*MoltVel)

            
            
        else:
            sogliaSX=area[:,15:200]
            NareaSX=(9000-np.count_nonzero(sogliaSX))/100/6
            
            #print(NareaH)
            
            if(NareaH>80):
                DXred2()
                dx15()
            
            Vmotori((30+NareaSX)*MoltVel,(30-NareaSX)*MoltVel)
           
        
        
        if(faseLastBasket == 0):
            
            
            #print(nera)
            
            #ho gia raccolto la bianca e ho una pallina nera vicina
            if(nera!=(0,0) and nera[0]>110 ):
                
                
                #if((giro == 1 and nera[1]<500) or (giro == 0 and nera[1]>300) or nera[0]>160):
                    
                    '''
                    if(giro == 0 and nera[1]<300):
                        dx30()
                        Vmotori(30,30)
                        time.sleep(3)
                        sx90
                        
                    if(giro == 1 and nera[1]>500):
                        sx30()
                        Vmotori(30,30)
                        time.sleep(2)
                        dx90()
                    '''
                    print('vista nera')
                    Cpresi=0
                    Cvicini = 0
                    
                    #inizio a muovermi verso la pallina
                    while 1:
                        tstart = time.time()
                        while (update==0):
                            time.sleep(0.001)
                        update = 0
                        
                        
                        
                        if(nera!=(0,0)):
                            Cpresi=0
                            #calcolo motori
                            ErroreY = 200-nera[0]
                            
                            deltaYo = ostacolo[0]-nera[0]
                            
                            if (giro == 1):
                                ErroreX = 550-nera[1]
                            else:
                                ErroreX = 250-nera[1]
                            
                                
                            #aspetto di centrare la pallina prima di andarci in contro
                            if(ErroreX<80 and ErroreX>-80):
                                Ky=0.6
                                Kx=0.5

                            else:
                                Ky=0.2
                                Kx=0.5
                            
                            Vsx=ErroreY*Ky+ErroreX*Kx
                            Vdx=ErroreY*Ky-ErroreX*Kx
                            
                            Vsx=np.clip(Vsx,-30,30)
                            Vdx=np.clip(Vdx,-30,30)
                            Vmotori(Vsx,Vdx)
                            
                            cv2.imshow('img',imgDetector)
                            cv2.waitKey(1)&0xff
                            
                            #break quando vicino
                            if(ErroreY<20 and ErroreY>-20 and ErroreX<20 and ErroreX>-20):
                                Cvicini+=1
                                
                                if(Cvicini>10):
                                    break
                                
                            else:
                                Cvicini=0
                        else:
                            Vmotori(0,0)
                            Cpresi+=1
                            if(Cpresi>20):
                                print('pallina nera persa di vista',nera,bianca)
                                #cv2.imshow('persa',imgDetector)
                                #cv2.waitKey(0)
                                break
                    
                        print('fps raccolta nera:',1/(time.time()-tstart))
                    if(Cpresi == 0):
                        img = foto()
                        gray = cv2.cvtColor(img[300:400,:], cv2.COLOR_BGR2GRAY)
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

                                        
                        M = cv2.moments(area)
                        cX = 0
                        cY = 0
                        if(M["m00"]!=0):
                            cX = int(M["m10"] / M["m00"])-400
                        else:
                            cX = 0
                            
                        print(cX)
                        
                        if(cX<-30 and giro == 1):
                            sxT(1)
                            Vmotori(40,40)
                            time.sleep(1.5)
                            dxT(3)
                        #cv2.imshow('area',area)
                        #cv2.waitKey(0)
                        
                        StatoDetector = 0
                        RaccoltaPallina('nera')
                        Vmotori(0,0)
                        time.sleep(0.5)
                        StatoDetector = 1
                        time.sleep(0.1)
                        
                        
            
            #vedo una pallina bianca non lontana
            if(bianca!=(0,0) and bianca[0]>110):
                Cvicini = 0
                if((giro == 1 and bianca[1]<500) or (giro == 0 and bianca[1]>300) or bianca[0]>210):
                    
                    print('vista bianca')
                    Cpresi=0
                    Cvicini = 0
                    #inizio a muovermi verso la pallina
                    Cpresi=0
                    while 1:
                        TinFPS = time.time()
                        while (update==0):
                            time.sleep(0.001)
                        update = 0
                        
                        if(bianca!=(0,0)):
                            #print(bianca,'vista')
                            Cpresi=0
                            #calcolo motori
                            ErroreY = 200-bianca[0]
                            
                            if (giro == 1):
                                ErroreX = 550-bianca[1]
                                #ErroreX = 400-bianca[1]
                            else:
                                ErroreX = 250-bianca[1]
                                #ErroreX = 400-bianca[1]
                            #aspetto di centrare la pallina prima di andarci in contro
                            if(ErroreX<80 and ErroreX>-80):
                                Ky=0.6
                                Kx=0.5
                            else:
                                Ky=0.2
                                Kx=0.3
                            
                            Vsx=ErroreY*Ky+ErroreX*Kx
                            Vdx=ErroreY*Ky-ErroreX*Kx
                            
                            Vsx=np.clip(Vsx,-30,30)
                            Vdx=np.clip(Vdx,-30,30)
                            Vmotori(Vsx,Vdx)
                            
                            cv2.imshow('img',imgDetector)
                            cv2.waitKey(1)&0xff
                            
                            #break quando vicino
                            if(ErroreY<20 and ErroreY>-20 and ErroreX<20 and ErroreX>-20):
                                Cvicini+=1
                                
                                if(Cvicini>10):
                                    break
                                
                            else:
                                Cvicini=0
                        else:
                            Vmotori(0,0)
                            
                            Cpresi+=1
                            if(Cpresi>20):
                                print('pallina bianca persa di vista AAA')
                                break
                        print('fps_fase2:',1/(time.time()-TinFPS))
                        
                    if(Cpresi == 0):
                        
                        print('avvio raccolta pallina')
                        StatoDetector = 0
                        time.sleep(0.5)
                        RaccoltaPallina('bianca')
                        Vmotori(0,0)
                        time.sleep(0.5)
                        StatoDetector = 1
                        time.sleep(0.1)
                        
            if(ostacolo!=(0,0) and ostacolo[0]> 250 and ostacolo[1]>100 and  ostacolo[1]<700):
                
                
                Cvicini=0
                print('ostacolo immezzo da raggirare',ostacolo)
                
                while 1:
                    while (update==0):
                        time.sleep(0.001)
                    update = 0
                    
                    if(ostacolo!=(0,0)):
                        CostPersi = 0
                        ErroreY = 415-ostacolo[0]
                        ErroreX = 400-ostacolo[1]
                        
                        Vsx=ErroreY*0.4+ErroreX*0.4
                        Vdx=ErroreY*0.4-ErroreX*0.4
                        
                        Vsx=np.clip(Vsx,-30,30)
                        Vdx=np.clip(Vdx,-30,30)
                        
                        
                        Vmotori(Vsx,Vdx)
                        
                        if(ErroreY<30 and ErroreY>-30 and ErroreX<40 and ErroreX>-40):
                            Cvicini+=1
                            
                            if(Cvicini>10):
                                
                                if (PosOstacolo == 'lato'):
                                    if(giro==1):
                                        dx90()
                                        dx90()
                                        giro = 0
                                        
                                    else:
                                        dx90()
                                        dx90()
                                        giro = 1
                                        
                                else:
                                    if(giro==1):
                                        Vmotori(-30,30)
                                        time.sleep(1.5)
                                        Vmotori(0,0)
                                    else:
                                        Vmotori(30,-30)
                                        time.sleep(1.3)
                                        Vmotori(0,0)
            
                                break
                        else:
                            Cvicini=0
                    else:
                        CostPersi+=1
                        Vmotori(0,0)
                        if(CostPersi>10):
                            break
                    cv2.imshow('img',imgDetector)
                    cv2.waitKey(1)&0xff
                            
                Vmotori(0,0)
                #time.sleep(10)
            
            
            
            cv2.imshow('img',img)
            #cv2.imshow('hsv',hsv)
            #cv2.imshow('maskDX',maskDX)
            cv2.waitKey(1)&0xff
            #cv2.waitKey(0)
    
        
          
        #print(1/(time.time()-t1))
    
                   
if(__name__ == '__main__'):
    

    
    global giro
    giro = 1
    
    print('in main stanza')
    #scaricoDX()
    #time.sleep(111111)
    try:
        stopStream()
    except:
        print('non ho stoppato la streaminag')
    
    avvioStreamHD()
    print('qwecad')
    esci()
    #scaricaPalline()
    #trovaUschita()
    #print('out da eschi')
    #DXred()
    #scaricoPalline()
    
    #cameraSu()
    #RaccoltaPallina('bianca')
    #errore*=0
    #DXred()
    
    #scaricaPalline()
    
    #stanza()
    #cv2.destroyAllWindows()
    #gotoStart(0)
    #scaricaPalline()

    #SXred()
    print('main stanza')
    
    #avvioStreamHD()
    #time.sleep(1111111)
    

    print('main stanza2')
    while 1:
        
        img=foto()
        #print('main stanza3')
       
        
        #maschera bordi stanza
        hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        #rosso = cv2.inRange(hsv, lower_red, upper_red)
        #rosso += cv2.inRange(hsv, lower_red2, upper_red2)

        #Vmotori(30,30)
        #time.sleep(0.3)
        
        
        green = cv2.inRange(hsv, lower_green, upper_green)
        #print(np.count_nonzero(green))
        #cv2.imshow('rosso',rosso)
        cv2.imshow('hsv',hsv)
        cv2.imshow('img',img)
        cv2.imshow('green',green)
        
        cv2.waitKey(1)&0xff

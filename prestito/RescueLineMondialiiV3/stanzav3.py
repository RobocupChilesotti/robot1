import cv2
import numpy as np
from detector2 import palline
from robot import Vmotori
from cattura import foto
from Semplifica import semplifica
from cattura import avvioStream128
from cattura import avvioStreamHD
from cattura import stopStream
#from robot import cameraSu
#from robot import cameraGiu
#from robot import caricoDX
#from robot import caricoSX
#from robot import scaricoSX
#from robot import scaricoDX
#from robot import distanceAV
#from robot import cameraSuFAST
from threading import Thread
import time
from detector2 import palline

#cameraSu()
#avvioStreamHD()

sigma=10


def show(img):
    cv2.imshow('img2',img)
    cv2.waitKey(1)&0xff


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
    



global ricerca
ricerca=1

global imgMov
imgMov=foto()

global allineamento
allineamento=0

global delta
delta=0 

def movimentoRandom():
    global imgMov

    global ricerca
    
    
    kernel = np.ones((5,5),np.uint8)
    kernel2 = np.ones((25,25),np.uint8)
    imgB=np.zeros((600,800),dtype=np.uint8)
    while 1:
        
        if(ricerca==0):
            Vmotori(0,0)
            print('STOP ricerca')
            #return
            while(ricerca==0):
                time.sleep(0.1)
        
        t1=time.time()
        
        img=foto()
        
        
        
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
        
        img=cv2.rectangle(img,(600,200),(785,300),(0,0,255),thickness=1)
        #img=cv2.rectangle(img,(15,200),(100,400),(0,0,255),thickness=1)
        
        img=cv2.rectangle(img,(200,200),(600,300),(255,0,0),thickness=1)
        
        sogliaDX=area[:,600:785]
        
        sogliaH=area[:,200:600]
        
        
        NareaH=(40000-np.count_nonzero(sogliaH))/93
        
        #print(np.count_nonzero(sogliaDX))
        NareaDX=(9000-np.count_nonzero(sogliaDX))/100/4
        #NareaDX=(13000-np.count_nonzero(sogliaDX))/100/4
        #NareaDX=(17000-np.count_nonzero(sogliaDX))/100/4
        
        Vmotori(30+NareaDX+NareaH,30-NareaDX-NareaH)
        
        imgMov=img.copy()
        #show(img)
        cv2.imshow('img',img)
        #cv2.imshow('sogliaDX',sogliaDX)
        #cv2.imshow('sogliaSX',sogliaSX)
        #cv2.imshow('sogliaH',sogliaH)
        #cv2.imshow('area',area)
                                        


        cv2.waitKey(1)&0xff
        
        print(1/(time.time()-t1))
            

def Posizionamento():
    StatoPos=0
    Tin=time.time()
    c=0
    Cout=0
    Ymax=0
    while 1:
        
        if(c>6):
            break
        
        stato,pos,dim,img,tipo=palline()
        
        if(pos[0]>510):
            break
        
        #if(pos[0]>450)
        
        #show(img)
        #cv2.imshow('img2',img)
        
        cv2.imshow('img',img)

        cv2.waitKey(1)&0xff

        if(stato==0):
            Vmotori(-15,-15)
            Cout+=1
            if(Cout>60):
                break
        else:
            Cout=0
            if(StatoPos==0):
                ErroreX=pos[1]-450
                ErroreY=pos[0]-520
            else:
                ErroreX=pos[1]-300
                ErroreY=pos[0]-270
            #print(ErroreY,StatoPos)
                
            if(StatoPos==0 and pos[0]>Ymax):
                Ymax=pos[0]
            
            if(pos[0]<Ymax-20 and StatoPos==0):
                Vmotori(-7,7)
                print('scendo dal muro')
                time.sleep(1)
                break
                
            
            
            if((ErroreY<20 and ErroreY>-20) or time.time()-Tin>3):
                c+=1
                if(StatoPos==0):
                    Tin=time.time()
                    StatoPos=1
                    
                    
                else:
                    StatoPos=0
                    Tin=time.time()
                    Ymax=0
            Vdx=-ErroreX*0.35-ErroreY*0.35 #-IErroreX*0-IErroreY*0 - (ErroreX-ErroreXPre)*0 - (ErroreY-ErroreYPre)*0
            Vsx=+ErroreX*0.35-ErroreY*0.35 #+IErroreX*0-IErroreY*0 + (ErroreX-ErroreXPre)*0 - (ErroreY-ErroreYPre)*0
        
            Vdx=np.int16(Vdx)
            Vsx=np.int16(Vsx)
        
            Vmotori(Vdx,Vsx)  


    cameraSuFAST()

    
#Posizionamento()

def stanza():

    global ricerca

    global imgMov
    imgMov=foto()

    global allineamento


    c=0

    mov=Thread(target=movimentoRandom,args=())
    mov.start()

    time.sleep(100000)


    UltimaRaccolta=time.time()
    while 1:

        GiaAllineato=0

        cv2.imshow('img',imgMov)
        cv2.waitKey(1)&0xff
        stato,pos,dim,img,tipo=palline()
        
        if(stato>=1):
            c+=1
        else:
            c=0
        
        #print(pos[0])
        

        if(c>5 and (pos[1]<300 or pos[0]>150)):
            c2=0
            c3=0
            #cv2.destroyAllWindows()
            print('trovata pallina')
            ricerca=0
            
            #mov.join()
            Vmotori(0,0)
            #print('join')
            time.sleep(1)
            Vmotori(0,0)
            
            ErroreYPre=pos[0]-370
            ErroreXPre=pos[1]-400
            
            c4=0
            
            Tin=time.time()
            
            while 1:
                

                
                stato,pos,dim,img,tipo=palline()
                #show(img)
                #cv2.imshow('img2',img)
                img=cv2.circle(img,(int(pos[1]),int(pos[0])),15,(0,0,255),thickness=-1)
                img=cv2.circle(img,(400,370),25,(0,250,),thickness=4)
                
                cv2.imshow('img',img)

                cv2.waitKey(1)&0xff

                if(stato==0):
                    print(c3)
                    c3+=1
                    print(c2)
                    Vmotori(0,0)
                    if(c3>10):
                        Vmotori(0,0)
                        ricerca=1
                        print('out')
                        break
                else:
                    c3=0
                    
                    ErroreY=pos[0]-370
                    ErroreX=pos[1]-400
                    
                
                    distanza=(ErroreY-ErroreYPre)**2+(ErroreX-ErroreXPre)**2
                
                    
                    if(distanza<20 and time.time()-Tin>4):
                        c4+=1
                    else:
                        c4=0
                      
                    if(c4>40 and pos[0]<400 and 0):
                        Posizionamento()
                        c2=0
                        c4=0
                        
                    if(ErroreY>-20):
                        ErroreX=np.clip(ErroreX,-50,50)
                    Vdx=-ErroreX*0.45-ErroreY*0.45 #-IErroreX*0-IErroreY*0 - (ErroreX-ErroreXPre)*0 - (ErroreY-ErroreYPre)*0
                    Vsx=+ErroreX*0.45-ErroreY*0.45 #+IErroreX*0-IErroreY*0 + (ErroreX-ErroreXPre)*0 - (ErroreY-ErroreYPre)*0

                    Vmax=np.amax((Vdx,Vsx,-Vdx,-Vsx))
                    
                    if(Vmax>30):
                        Vdx=Vdx*30/Vmax
                        Vsx=Vsx*30/Vmax
                        
                    else:
                        if(Vmax<10 and distanza>10):
                            Vdx=Vdx*10/Vmax
                            Vsx=Vsx*10/Vmax
                    

                    #print(IErroreX,ErroreX)

                    
                    Vdx=np.int16(Vdx)
                    Vsx=np.int16(Vsx)
                    
                    if(ErroreX<10 and ErroreX>-10 and ErroreY<10 and ErroreY>-10):
                        c2+=1
                    else:
                        c2=0
                    
                    if(c2>20):
                        print(ErroreX,ErroreY)

                        if(GiaAllineato==0 and 0):
                            Posizionamento()
                            GiaAllineato=1
                        else:

                        
                            Vmotori(-20,-20)
                            time.sleep(1)
                            Vmotori(0,0)
                            
                            
                            
                            if(tipo==1):
                                caricoSX()
                            else:
                                caricoDX()
                                
                            #scaricoDX()
                            
                            time.sleep(1)
                            
                            Vmotori(0,0)
                            ricerca=1
                            GiaAllineato=0
                            UltimaRaccolta=time.time()
                            break
                
                    
                    Vmotori(Vdx,Vsx)
                    
                    ErroreYPre=ErroreY
                    ErroreXPre=ErroreX
                    

                    
        
        if(time.time()-UltimaRaccolta>350000000000):
            print('fine raccolta palline')
            ricerca=0
            break
        

    while 1:
        
        img=foto()
        img=img[100:400,500:800,1]
        
        img[img<40]=0
        img[img>39]=255

        
        img=255-img
        
        
        imgMov[100:400,500:800,0]=img
        cv2.imshow('img',imgMov)
        cv2.waitKey(1)&0xff
            

        if(np.count_nonzero(img)>30000):
            ricerca=0
            #mov.join()
            Vmotori(0,0)
            #print('join')
            time.sleep(0.5)
            
            Vmotori(30,30)
            time.sleep(2)
            
            Vmotori(-30,30)
            time.sleep(2)
            
            Vmotori(30,30)
            time.sleep(4)
            
            Vmotori(-30,-30)
            time.sleep(0.5)
            
            Vmotori(30,-30)
            time.sleep(4)
            
            Vmotori(-30,-30)
            time.sleep(2)
            
            Vmotori(0,0)
            
            scaricoSX()
            scaricoDX()
            
         
if __name__ == '__main__':
    avvioStreamHD()
    stanza()
       

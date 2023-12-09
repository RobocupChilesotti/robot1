import cv2
import numpy as np
from threading import Thread
from robot import Vmotori
from cattura import foto
from Semplifica import semplifica
from cattura import avvioStream128
from cattura import avvioStreamHD
from cattura import stopStream
from robot import cameraGiu
from robot import cameraSu
from stanzav3 import stanza

print('End inport')


import time

from main import startPage
startPage()
import variabili

avvioStream128()
#cameraGiu()
time.sleep(1)


global risX
risX = 128  #deve essere pari
global risY
risY = 128  #deve essere pari
global X
X = 1   #define per essere comodi lavorando con array
global Y
Y = 0
global Xmezzo
Xmezzo = np.uint8((risX+risY*2)/2)
global SpessoreMax
SpessoreMax = 15  #numero di pixel massimi di spessore della linea, viene usato per cancellare le diramazioni inutili
global imgW
imgW=np.ones(shape=(risY,risX),dtype=np.uint8)*255
global imgB
imgB=np.zeros(shape=(risY,risX),dtype=np.uint8)
global imgONE
imgONE=np.ones(shape=(risY,risX),dtype=np.uint8)
global imgB_BIG
imgB_BIG=np.zeros(shape=(risY+40,risX+40),dtype=np.uint8)
#cosa da usare per filtrare le maschere e rimuovere i bordi
corniceIN=np.zeros(shape=(risX,risY),dtype=np.uint8)
corniceIN[10:risY-16,15:risX-16]=1

corniceOUT=np.ones(shape=(risX,risY),dtype=np.uint8)
corniceOUT[15:risY-16,15:risX-16]=0

#Vmotori(30,-30)
#time.sleep(100)

def InputLineArrayGen(risY,risX):
    global BordoINf
    BordoINf=np.zeros(shape=(risX+risY*2,2),dtype=np.uint8)

    c=0
    for y in range(0,risY):
        BordoINf[c,X]=0
        BordoINf[c,Y]=y
        c+=1

    for x in range(risX):
        BordoINf[c,X]=x
        BordoINf[c,Y]=risY-1
        c+=1

    for y in range(risY-1,-1,-1):
        BordoINf[c,X]=risX-1
        BordoINf[c,Y]=y
        c+=1

def FX(c):
    return(BordoINf[c+Xmezzo,X])

def FY(c):
    return(BordoINf[c+Xmezzo,Y])

def reverse(coordinate):
    return (coordinate[1],coordinate[0])

def sommaVett(point,fase,modulo):
    p0=point[0]+np.cos(np.deg2rad(fase))*modulo
    p1=point[1]+np.sin(np.deg2rad(fase))*modulo
    return (p0,p1)

def Distanza2punti(p1y,p1x,p2y,p2x):
    return ((p1x-p2x)**2+(p1y-p2y)**2)**0.5


print('In Rescue Line')

if __name__ == '__main__':

    #genero l' array che utilizzo per il traking del primo punto della linea
    InputLineArrayGen(risY,risX)

    pos=-15 #posizione iniziale linea

    maskOutput=imgB.copy()

    variabileSacrificale=imgB.copy()

    tickPersi=0

    outrputX=64
    outrputY=0

    imgP=np.zeros((risY,risX,3),dtype=np.uint8)

    
    VerdiDaCangellarePre=imgB.copy()
    VerdiDaTenerePre=imgB.copy()
    
    cX=64
    cY=64

    Cstanza=0
    
    while(1):
        stato='inizio'
        t=time.time()
        img=foto()
        mask,b,green,r,s=semplifica(img.copy())
        maskOG=mask.copy()
    
        if(np.count_nonzero(s)>30):
            Cstanza+=1
        else:
            Cstanza=0
        
        if(Cstanza>5):
            Vmotori(30,30)
            Cstanza=0
            stopStream()
            cameraSu()
            avvioStreamHD()
            Vmotori(30,30)
            time.sleep(0.5)
            stanza()


        #rimuovo un incrocio troppo basso che creerebbe problemi
        amount, labels = cv2.connectedComponents(mask)
        IncrocioBasso=0
        for i in range(1,amount):
            maskArea=imgB.copy()
            maskArea[labels == i] = 255
            #se l'area bianca é troppo piccola la cancello
            if(np.count_nonzero(maskArea)<300):
                mask-=maskArea
                IncrocioBasso=1

        mask=255-mask
        #rimuovo i punti neri piú piccoli di 1/3 del magiore
        amount, labels = cv2.connectedComponents(mask)
        areaPezzoLineaMAX=0
        for i in range(1,amount):
            #calcolo l'area di tutti i punti
            maskArea=imgB.copy()
            maskArea[labels == i] = 255
            areaPezzoLinea=np.count_nonzero(maskArea)
            #trovo quello massimo
            if(areaPezzoLinea>areaPezzoLineaMAX):
                areaPezzoLineaMAX=areaPezzoLinea

        #ottimizzabile:faccio 2 vote gli stessi calcoli e porei salvarli e non rifarli'
        #cancello i punti minori di 1/3 area max
        for i in range(1,amount):
            #calcolo l'area di tutti i punti
            maskArea=imgB.copy()
            maskArea[labels == i] = 255
            areaPezzoLinea=np.count_nonzero(maskArea)
            #cancello se un pezzo nero é troppo piccolo
            if(areaPezzoLinea<areaPezzoLineaMAX/3):
                mask-=maskArea

        mask=255-mask

        kernel = np.ones((SpessoreMax,SpessoreMax),np.uint8)
        #ottimizabile: posso unirlo al primo punto
        #dilato e restringo ogni area bianca in modo da cancellare le linee che non portano a nulla
        amount, labels = cv2.connectedComponents(mask)
        for i in range(1,amount):
            #calcolo l'area di tutte le aree bianche rimaste
            maskAreaPre=imgB.copy()
            maskArea=imgB_BIG.copy()
            maskAreaPre[labels == i] = 255
            maskArea[20:risY+20,20:risX+20]=maskAreaPre
            maskArea = cv2.dilate(maskArea,kernel,iterations = 1)
            maskArea = cv2.erode(maskArea,kernel,iterations = 1)

            #cancello le linee che non portano a nulla che non siano nei bordi
            maskArea=maskArea[20:risY+20,20:risX+20]
            #maskArea=np.logical_and(maskArea,corniceIN)
            mask=np.logical_or(maskArea,mask)
            mask=np.uint8(mask)*255

        
        #trovo partenza linea
        if(mask[FY(pos),FX(pos)]==0):
            #mi trovo gia sulla line
            #print('sono giá in linea')
            StateDX=0
            StateSX=0

            point=np.clip(pos+19,-190,190)
            PdxLine=point
            point=np.clip(pos-19,-190,190)
            PsxLine=point

            for spostamento in range(300):
                #print(spostamento)
                
                #calcolo il punto di destra
                point=np.clip(pos+spostamento,-190,190)
                if(mask[FY(point),FX(point)]!=0 and StateDX==0):
                    PdxLine=point
                    StateDX=1
                
                #calcolo il punto di sinisra
                point=np.clip(pos-spostamento,-190,190)
                if(mask[FY(point),FX(point)]!=0 and StateSX==0):
                    PsxLine=point
                    StateSX=1

                if(StateSX and StateDX):
                    break
        else:
            #cerco la linea
            #print('cerco la linea')
            
            for spostamento in range(300):
                #print(spostamento)
                point=np.clip(pos+spostamento,-190,190)
                #print(mask[FY(point),FX(point)])
                if(mask[FY(point),FX(point)]==0):
                    PsxLine=point
                    #print(point)
                    while(mask[FY(point),FX(point)]==0):
                        #print('blocco',point)
                        spostamento+=1
                        point=np.clip(pos+spostamento,-190,190)
                        if(point==190 or point==-190):
                            break
                    PdxLine=point
                    break

                point=np.clip(pos-spostamento,-190,190)
                #print(mask[FY(point),FX(point)])
                if(mask[FY(point),FX(point)]==0):
                    PdxLine=point
                    while(mask[FY(point),FX(point)]==0):
                        #print('blocco',point)
                        spostamento+=1
                        point=np.clip(pos-spostamento,-190,190)
                        if(point==190 or point==-190):
                            break
                    PsxLine=point
                    break
        pos=int((PsxLine+PdxLine)/2)


        #ri calcolo le aree(cosi tengo conto dei punit che ho cancellato)
        amount, labels = cv2.connectedComponents(mask)
        #trobo l'indice che rappresenta l'area DX
        Ndx=labels[FY(PdxLine),FX(PdxLine)]
        areaDX=imgB.copy()

        if(Ndx!=0):
            areaDX[labels == Ndx] = 255

        Nsx=labels[FY(PsxLine),FX(PsxLine)]
        areaSX=imgB.copy()

        if(Nsx!=0):
            areaSX[labels == Nsx] = 255

        if(np.count_nonzero(areaSX//255*areaDX)>100):
            #gap
            #print('gap')
            kernel = np.ones((15,15),np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            
            M = cv2.moments(255-mask)
            if(M["m00"]!=0):
                cX = int(M["m10"] / M["m00"])-64
            else:
                cX=0
                
            Vmotori((20-cX)/50*variabili.vel,(20+cX)/50*variabili.vel)
            
            imgP[:,:,:]=0
            #aggiongo la linea
            imgP[:,:,0]+=mask
            imgP[:,:,1]+=mask
            imgP[:,:,2]+=mask
            
            
            imgP=cv2.circle(imgP,(cX+64,30),10,(255,0,0),thickness=-1)
            
            imgP2=cv2.resize(imgP,(256,256),dst=cv2.INTER_NEAREST)
            cv2.imshow('imgP',imgP2)
            #cv2.imshow('maskOutput',maskOutput)
            cv2.waitKey(1)&0xff
            
        else:

            #cv2.imshow('areaDX',areaDX)
            #cv2.imshow('areaSX',areaSX)

            #cancello i verdi vicino all' ingresso linea
            #green=cv2.circle(green,(FX(pos),FY(pos)),35,0,thickness=-1)



            #trovo e classifico tutti gli incroci


            #calcolo le aree bianche dopo le semplificazioni
            amount, labels = cv2.connectedComponents(mask)

            #0=Y
            #1=X
            #2=tipo
            #      0=T
            #      1=X


            kernel=np.ones((35,35),np.uint8)
            MaskIncroci=imgB.copy()

            #dilato tutte le aree e trovo dove si intersecano        
            for i in range(1,amount):
                maskArea=imgB.copy()
                maskArea[labels == i] = 255
                maskArea = cv2.dilate(maskArea,kernel,iterations = 1)
                maskArea//=5
                MaskIncroci+=maskArea

            

            MaskIncroci2=MaskIncroci.copy()

            

            ret,MaskIncroci2=cv2.threshold(MaskIncroci2,103,255,cv2.THRESH_BINARY)
            
            

            amount, labels = cv2.connectedComponents(MaskIncroci2)

            #salvo coordinate per grafica
            NdiIncroci=amount-1
            coordinateIncroci=np.zeros(shape=(amount-1,3),dtype=np.int16)

            for i in range(1,amount):
                Pincrocio=imgB.copy()
                Pincrocio[labels == i] = 255
                M = cv2.moments(Pincrocio)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                coordinateIncroci[i-1,0]=cY
                coordinateIncroci[i-1,1]=cX
                #e un incrocio a t
                if(MaskIncroci[cY,cX]==153):
                    coordinateIncroci[i-1,2]=0
                else:
                    coordinateIncroci[i-1,2]=1

                    







            #calcolo numero di punti verdi
            amount, labels = cv2.connectedComponents(green)
            
            verdeDX=0
            verdeSX=0

            #salvo coordinate per grafica
            coordinateVerde=np.zeros(shape=(amount-1,4),dtype=np.int16)

            numeroDiVerdi=amount-1

            VerdiDaCangellare=imgB.copy()
            VerdiDaTenere=imgB.copy()

            VerdiInfluenti=imgB.copy()

            for i in range(1,amount):
                Pvrde=imgB.copy()
                Pvrde[labels == i] = 255

                #calcolo centro X e Y di tutti i punti
                M = cv2.moments(Pvrde)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                #print(i)
                coordinateVerde[i-1,0]=cY
                coordinateVerde[i-1,1]=cX

                #valore da 0 a 255 che indica quanto un punto appartiene a una o un altra categoria in un punto
                ShoreCancella=VerdiDaCangellarePre[cY,cX]
                ShoreTenere=VerdiDaTenerePre[cY,cX]

                

                if(ShoreCancella!=0):
                    VerdiDaCangellare[Pvrde==255]=ShoreCancella
                if(ShoreTenere!=0):
                    VerdiDaTenere[Pvrde==255]=ShoreTenere

                if(areaSX[cY,cX]==255):
                    #calcolo se é un verde di sinistra
                    #vedo se fa parte dei verdi da canellare o no
                    if(ShoreCancella<=ShoreTenere):
                        verdeSX=1
                        #1=sinistra stato del verde in questione
                        coordinateVerde[i-1,2]=1
                        VerdiInfluenti+=Pvrde
                    VerdiDaTenere[Pvrde==255]=np.clip(ShoreTenere+10,0,255)
                else:
                    #calcolo se é un verde di destra
                    if(areaDX[cY,cX]==255):
                        #vedo se fa parte dei verdi da canellare o no
                        if(ShoreCancella<=ShoreTenere):
                            verdeDX=1
                            #2=sinistra stato del verde in questione
                            coordinateVerde[i-1,2]=2
                            VerdiInfluenti+=Pvrde
                        VerdiDaTenere[Pvrde==255]=np.clip(ShoreTenere+10,0,255)
                        

                    else:
                        VerdiDaCangellare[Pvrde==255]=np.clip(ShoreCancella+10,0,255)

                #segnio la differenza di punteggi per la grafica
                A=np.uint16(VerdiDaTenere[cY,cX])
                B=np.uint16(VerdiDaCangellare[cY,cX])
                valoreDeltaShore=np.uint16(A-B)
                if(valoreDeltaShore<0):
                    valoreDeltaShore=-valoreDeltaShore
                coordinateVerde[i-1,3]=valoreDeltaShore
            #cv2.imshow('VerdiDaCangellare',VerdiDaCangellare)
            #cv2.imshow('VerdiDaTenerePre',VerdiDaTenerePre)

            DoppioVerde=0

            if(verdeDX and verdeSX):
                #print('doppio verde1')
                #controllo se c'e un verde
                kernel=np.ones((30,30),dtype=np.uint8)
                #verde/i di desta dilatati
                areaVerdeDx=np.logical_and(areaDX,green,variabileSacrificale)*255
                
                if(np.count_nonzero(areaVerdeDx)<400):
                    areaVerdeDx[:,:]=0
                
                areaVerdeDx=cv2.dilate(areaVerdeDx,kernel,iterations=1)
                #verde/i di sinistra dilatati
                areaVerdeSx=np.logical_and(areaSX,green,variabileSacrificale)*255
                
                if(np.count_nonzero(areaVerdeSx)<400):
                    areaVerdeSx[:,:]=0
                
                areaVerdeSx=cv2.dilate(areaVerdeSx,kernel,iterations=1)

                #cv2.imshow('areaVerdeDx',areaVerdeDx)
                #cv2.imshow('areaVerdeSx',areaVerdeSx)
                

                intersezionDoppioVerde=np.logical_and(areaVerdeDx,areaVerdeSx,variabileSacrificale)*255
                #print(np.count_nonzero(intersezionDoppioVerde))
                #se i 2 verdi sono abbastanza vicini da generare un area abbastanza grande allora doppio verde
                if(np.count_nonzero(intersezionDoppioVerde)>150):
                    DoppioVerde=1
            
                #cv2.imshow('DoppioVerde',intersezionDoppioVerde)
                #cv2.imshow('dx',areaVerdeDx)
                #cv2.imshow('sx',areaVerdeSx)
                #Vmotori(0,0)
                #cv2.waitKey(0)
                #cv2.destroyAllWindows()
                #intersezionDoppioVerde=np.logical_or(areaVerdeDx,areaVerdeSx,variabileSacrificale)*255
                
                #se i 2 verdi sono abbastanza vicini da generare un area abbastanza grande allora doppio verde
                #if(np.count_nonzero(intersezionDoppioVerde)>1800):
                #    DoppioVerde+=1


            if(DoppioVerde==1):
                #print('doppio verde2')
                stato='doppio verde'
                Vmotori(-30,30)
                time.sleep(4)
                #Vmotori(-30,-30)
                #time.sleep(1)
            else:
                for i in range(NdiIncroci):
                    Xi=coordinateIncroci[i,1]
                    Yi=coordinateIncroci[i,0]
                    
                    distanza = Distanza2punti(Yi,Xi,FY(pos),FX(pos))

                    if(distanza>30):

                        if(coordinateIncroci[i,2]==0):
                            #incrocio a T
                            VerdiInfluenti2=VerdiInfluenti.copy()

                            AreaIncrocio=imgB.copy()
                            AreaIncrocio=cv2.circle(AreaIncrocio,(Xi,Yi),30,1,thickness=-1)
                            #verdi vicini all incrocio
                            VerdiInfluenti2*=AreaIncrocio

                            if(np.count_nonzero(VerdiInfluenti2)>10):
                                #incrocio a T con verde

                                kernel=np.ones((35,35),dtype=np.uint8)
                                LineaBuona=cv2.dilate(VerdiInfluenti2,kernel,iterations=1)-VerdiInfluenti2
                                LineaBuona*=AreaIncrocio
                                
                                LineaBuona[AreaIncrocio==0]=255
                                
                                mask=np.logical_and(255-mask,LineaBuona,variabileSacrificale)*255
                                mask=255-mask
                            else:
                                #incrocio a T senza verde
                                

                                AreeIncrocioT=AreaIncrocio*mask
                                amount, labels = cv2.connectedComponents(AreeIncrocioT)

                                

                                kernel=(20,20)
                                blurIncrocio=imgB_BIG.copy()
                                blurIncrocio+=255

                                blurIncrocio[20:148,20:148]=mask
                                blurIncrocio=cv2.blur(blurIncrocio,kernel)
                                ret,blurIncrocio = cv2.threshold(blurIncrocio,100,255,cv2.THRESH_BINARY)

                                blurIncrocio=blurIncrocio[20:148,20:148]
                                
                                blurIncrocio=np.logical_and(255-blurIncrocio,mask,variabileSacrificale)*255

                                cv2.imshow('blurIncrocio',blurIncrocio)

                                PuntiMin=10000

                                for i in range(1,amount):
                                    area=imgB.copy()
                                    area[labels==i]=255
                                    area=np.logical_and(area,blurIncrocio,variabileSacrificale)*255
                                    punti=np.count_nonzero(area)
                                    if(punti<PuntiMin):
                                        PuntiMin=punti
                                        indexPuntiMin=i
                                
                                area=imgB.copy()
                                area[labels==indexPuntiMin]=255
                                

                                kernel=np.ones((35,35),dtype=np.uint8)
                                area=cv2.dilate(area,kernel,iterations=1)
                                area=np.logical_and(area,255-mask,variabileSacrificale)*255
                                area=(255-area)*AreaIncrocio
                                #cv2.imshow('area',area)

                                mask=mask*np.logical_not(AreaIncrocio)+area

                                #area[AreaIncrocio==0]=mask

                        else:
                            #incrocio a X
                            #cv2.imshow('MaskIncrociXPre',MaskIncrociXPre)
                            '''
                            punti=MaskIncrociXPre[Yi,Xi]+10
                            punti=np.clip(punti,0,255)
                            
                            cerchio=imgB.copy()
                            cerchio=cv2.circle(cerchio,(Xi,Yi),20,255,thickness=-1)

                            MaskIncrociX[cerchio==255]=punti
                            '''
                            VerdiInfluenti2=VerdiInfluenti.copy()

                            AreaIncrocio=imgB.copy()
                            AreaIncrocio=cv2.circle(AreaIncrocio,(Xi,Yi),30,1,thickness=-1)
                            #verdi vicini all incrocio
                            VerdiInfluenti2*=AreaIncrocio

                            if(np.count_nonzero(VerdiInfluenti2)>10):
                                #incrocio a X con verde
                                kernel=np.ones((35,35),dtype=np.uint8)
                                LineaBuona=cv2.dilate(VerdiInfluenti2,kernel,iterations=1)-VerdiInfluenti2
                                LineaBuona*=AreaIncrocio
                                
                                LineaBuona[AreaIncrocio==0]=255
                                
                                mask=np.logical_and(255-mask,LineaBuona,variabileSacrificale)*255
                                mask=255-mask
                            else:
                                #incrocio a X con verde
                                AreaIncrocioSmall=imgB.copy()
                                AreaIncrocioSmall=cv2.circle(AreaIncrocioSmall,(Xi,Yi),20,1,thickness=-1)
                                MaskIncrocoX=255-mask
                                MaskIncrocoX*=AreaIncrocio-AreaIncrocioSmall
                                #cv2.imshow('MaskIncrocoX',MaskIncrocoX)

                                amount, labels = cv2.connectedComponents(MaskIncrocoX)

                                Xin=FX(pos)
                                Yin=FY(pos)


                                distanze= np.zeros((amount-1),dtype=np.float)

                                for i in range(1,amount):
                                    
                                    putoIncrocio=imgB.copy()
                                    putoIncrocio[labels==i]=255


                                    M = cv2.moments(putoIncrocio)
                                    cX = int(M["m10"] / M["m00"])
                                    cY = int(M["m01"] / M["m00"])

                                    distanza=Distanza2punti(cX,cY,Xin,Yin)
                                    distanze[i-1]=distanza


                                #print(distanze)

                                distanzaMax=np.amax(distanze)
                                distanzaMin=np.amin(distanze)



                                mask=255-mask

                                mask*=1-(AreaIncrocio-AreaIncrocioSmall)

                                
                                for i in range(1,amount):
                                    if(distanze[i-1]==distanzaMin):
                                        putoIncrocio=imgB.copy()
                                        putoIncrocio[labels==i]=255
                                        mask+=putoIncrocio
                                    if(distanze[i-1]==distanzaMax):
                                        putoIncrocio=imgB.copy()
                                        putoIncrocio[labels==i]=255
                                        mask+=putoIncrocio
                                    

                                mask=255-mask

                        #cv2.imshow('MaskIncrociX',MaskIncrociX)                  

            kernel = np.ones((SpessoreMax,SpessoreMax),np.uint8)
            #ottimizabile: facco gia una volta questo passaggio
            #dilato e restringo ogni area bianca in modo da cancellare le linee che non portano a nulla
            amount, labels = cv2.connectedComponents(mask)
            for i in range(1,amount):
                #calcolo l'area di tutte le aree bianche rimaste
                maskAreaPre=imgB.copy()
                maskArea=imgB_BIG.copy()
                maskAreaPre[labels == i] = 255
                maskArea[20:risY+20,20:risX+20]=maskAreaPre
                maskArea = cv2.dilate(maskArea,kernel,iterations = 1)
                maskArea = cv2.erode(maskArea,kernel,iterations = 1)

                #cancello le linee che non portano a nulla che non siano nei bordi
                maskArea=maskArea[20:risY+20,20:risX+20]
                #maskArea=np.logical_and(maskArea,corniceIN)
                mask=np.logical_or(maskArea,mask)
                mask=np.uint8(mask)*255

            mask=255-mask
            #rimuovo i punti neri piú piccoli di 1/3 del magiore
            amount, labels = cv2.connectedComponents(mask)
            areaPezzoLineaMAX=0
            for i in range(1,amount):
                #calcolo l'area di tutti i punti
                maskArea=imgB.copy()
                maskArea[labels == i] = 255
                areaPezzoLinea=np.count_nonzero(maskArea)
                #trovo quello massimo
                if(areaPezzoLinea>areaPezzoLineaMAX):
                    areaPezzoLineaMAX=areaPezzoLinea

            #cancello i punti minori di 1/3 area max
            for i in range(1,amount):
                #calcolo l'area di tutti i punti
                maskArea=imgB.copy()
                maskArea[labels == i] = 255
                areaPezzoLinea=np.count_nonzero(maskArea)
                #cancello se un pezzo nero é troppo piccolo
                if(areaPezzoLinea<areaPezzoLineaMAX/3):
                    mask-=maskArea

            mask=255-mask
                


            #cancello la linea di inizio
            cancelloIn=imgW.copy()
            cancelloIn=cv2.circle(cancelloIn,(FX(pos),FY(pos)),35,0,thickness=-1)
            #tengo un area vicina a quella da cui vengo
            tengoOut=imgB.copy()
            tengoOut=cv2.circle(tengoOut,(outrputX,outrputY),30,255,thickness=-1)
        

            #cornice estrerna and mask and (non ingresso)
            maskOutput=np.logical_and(255-mask,np.logical_and(cancelloIn,corniceOUT),variabileSacrificale)*255
            
            #cancello i punit non vicini alla posizione precedente della linea ma tengo tutte le informazion in caso la perdessi
            maskOutputTOT=maskOutput.copy()
            maskOutput=np.logical_and(maskOutput,tengoOut,variabileSacrificale)*255

            M = cv2.moments(maskOutput)
            if(np.sum(maskOutput)/255>10):
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                outrputX=cX
                outrputY=cY
                tickPersi=0
            else:
                #print('perso')
                tickPersi+=1

            if(tickPersi>4):    
                    M = cv2.moments(maskOutputTOT)
                    if( M["m00"]!=0):
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])
                    outrputX=cX
                    outrputY=cY


            deltaOutX=cX-64
            #deltaInX=64-FX(pos)
            
            deltaOutY=cY-64
            #deltainY=128-FY(pos)
            
            deltaX=-deltaOutX/2
            #deltaY=np.clip(deltaY,-20,30)
            
            deltaY=-deltaOutY/4
            #deltaX=np.clip(deltaX,-50,50)
            
            Vmotori((deltaY+deltaX)*variabili.vel/25,(deltaY-deltaX)*variabili.vel/25)


            #Vmotori(variabili.vel-50,variabili.vel-50)
         
            #grafica

            imgP[:,:,:]=0
            #aggiongo la linea
            imgP[:,:,0]+=mask
            imgP[:,:,1]+=mask
            imgP[:,:,2]+=mask

            #coloro le aree DX e SX
            areaSX=np.uint8(areaSX//5)
            areaDX=np.uint8(areaDX//5)

            imgP[:,:,1]-=areaSX
            imgP[:,:,2]-=areaSX

            imgP[:,:,0]-=areaDX
            imgP[:,:,1]-=areaDX

            #cerchi nei punti iniziali
            imgP=cv2.circle(imgP,(FX(pos),FY(pos)),10,(255,0,255),thickness=3)
            imgP=cv2.circle(imgP,(FX(PdxLine),FY(PdxLine)),5,(0,0,255),thickness=-1)
            imgP=cv2.circle(imgP,(FX(PsxLine),FY(PsxLine)),5,(255,0,0),thickness=-1)

            lineeCancellate=np.logical_or(255-mask,maskOG,variabileSacrificale)*128
            lineeCancellate=128-lineeCancellate
            #cv2.imshow('lineeCancellate',lineeCancellate)
            #aggiongo le parti cancellate in gregio
            imgP[:,:,0]-=lineeCancellate
            imgP[:,:,1]-=lineeCancellate
            imgP[:,:,2]-=lineeCancellate

            #cerchio parte finale
            imgP=cv2.circle(imgP,(outrputX,outrputY),25,(0,200,200),thickness=2)

            if(stato=='incrocioT'):
                #cv2.imshow('a',areaDXBlur)
                imgP[areaDXBlur==255,1]=0
                imgP[areaDXBlur==255,0]=0
                imgP[areaSXBlur==255,1]=0
                imgP[areaSXBlur==255,2]=0

            imgP[green==255,0]=0
            imgP[green==255,1]=255
            imgP[green==255,2]=0
            #imgP[VerdiDaCangellare==255,1]=155


            #cerchi che indicano le classificazioni dei verdi
            for j in range(numeroDiVerdi):
                Xpv=coordinateVerde[j,1]
                Ypv=coordinateVerde[j,0]

                raggio=coordinateVerde[j,3]//25
                #print(raggio)
                if(raggio<0):
                    raggio=-raggio

                tipo=coordinateVerde[j,2]

                if(tipo==0):
                    imgP=cv2.circle(imgP,(Xpv,Ypv),raggio,(0,155,0),thickness=-1)

                if(tipo==1):
                    imgP=cv2.circle(imgP,(Xpv,Ypv),raggio,(255,0,0),thickness=-1)

                if(tipo==2):
                    imgP=cv2.circle(imgP,(Xpv,Ypv),raggio,(0,0,255),thickness=-1)

            for j in range(NdiIncroci):
                Xi=coordinateIncroci[j,1]
                Yi=coordinateIncroci[j,0]

                if(coordinateIncroci[j,2]==0):
                    imgP=cv2.circle(imgP,(Xi,Yi),30,(0,255,255))
                else:
                    imgP=cv2.circle(imgP,(Xi,Yi),30,(255,255,0))

            imgP[maskOutput==255,1]=150
            imgP[maskOutput==255,2]=250

            imgP2=cv2.resize(imgP,(256,256),dst=cv2.INTER_NEAREST)
            
            cv2.imshow('imgP',imgP2)
            #cv2.imshow('maskOutput',maskOutput)
            cv2.waitKey(1)&0xff


            
            VerdiDaCangellarePre=VerdiDaCangellare.copy()
            VerdiDaTenerePre=VerdiDaTenere.copy()

            VerdiDaCangellarePre[VerdiDaCangellarePre>5]-=5
            VerdiDaTenerePre[VerdiDaTenerePre>5]-=5

        print('fps: ',1/(time.time()-t))



    print(300/(time.time()-t))
    print('end')
    imgHD=cv2.resize(imgP,(500,500))
    cv2.imshow('coso',imgHD)
    cv2.waitKey(0)

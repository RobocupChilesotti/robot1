import numpy as np


'''VARIABILI UTILI'''
#Estrarre le variabili e porle qua dal file

#principale
vel=np.loadtxt("variabili/vel.txt", delimiter='\t')
avc=np.loadtxt("variabili/avc.txt", delimiter='\t')
camera_mode=np.loadtxt("variabili/camera_mode.txt", delimiter='\t')




        


#stanza
stanza_mode=0
stanza_uscita = open('variabili/stanza_uscita.txt', 'r').read().replace('\n', '')

#ostacolo
ostacolo_mode=np.loadtxt("variabili/ostacolo_mode.txt", delimiter='\t')
ostacolo_angolo=np.loadtxt("variabili/ostacolo_angolo.txt", delimiter='\t')
ostacolo_direzione=np.loadtxt("variabili/ostacolo_direzione.txt", delimiter='\t')


'''VARIABILI GLOBALI DA NON TOCCARE'''
nuova_uscita = open('variabili/stanza_uscita.txt', 'r').read().replace('\n', '')


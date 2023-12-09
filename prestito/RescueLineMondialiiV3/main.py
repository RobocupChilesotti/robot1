#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 5.4
#  in conjunction with Tcl version 8.6
#    Aug 08, 2020 10:14:06 AM CEST  platform: Windows NT

from threading import Thread
import sys
import variabili
import numpy as np
from PIL import Image,ImageTk
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import main_support

def f():
    while 1:
        print(variabili.avc)


global variabili


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global w, root
    root = tk.Tk()
    top = Toplevel1 (root)
    main_support.init(root, top)
    root.mainloop()

w = None
def create_Toplevel1(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_Toplevel1(root, *args, **kwargs)' .'''
    global w, root
    #rt = root
    root = rt
    w = tk.Toplevel (root)
    top = Toplevel1 (w)
    main_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Toplevel1():
    global w
    w.destroy()
    w = None

class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("600x450+650+150")
        top.minsize(120, 1)
        top.maxsize(1924, 1061)
        top.resizable(1, 1)
        top.title("Zin")
        top.configure(background="#d9d9d9")
        self.MainPage()

    def MainPage(self,top = None):
        self.main = tk.Frame(top)
        self.main.place(relx=0.01, rely=0.011, relheight=0.98, relwidth=0.98)
        self.main.configure(relief='groove')
        self.main.configure(borderwidth="2")
        self.main.configure(relief="groove")
        self.main.configure(background="#d9d9d9")

        self.Salva = tk.Button(self.main)
        self.Salva.place(relx=0.31, rely=0.885, height=24, width=47)
        self.Salva.configure(activebackground="#ececec")
        self.Salva.configure(activeforeground="#000000")
        self.Salva.configure(background="#00ff00")
        self.Salva.configure(disabledforeground="#a3a3a3")
        self.Salva.configure(foreground="#000000")
        self.Salva.configure(highlightbackground="#d9d9d9")
        self.Salva.configure(highlightcolor="black")
        self.Salva.configure(pady="0")
        self.Salva.configure(text='''Salva''')
        self.Salva.configure(command=self.SalvaTutto)

  

        self.camera_scale = ttk.Scale(self.main, from_=0, to=1)
        self.camera_scale.place(relx=0.44, rely=0.556, relwidth=0.1, relheight=0.0, height=36, bordermode='ignore')
        self.camera_scale.set(variabili.camera_mode)

        self.mode = tk.Label(self.main)
        self.mode.place(relx=0.35, rely=0.567, height=26, width=49)
        self.mode.configure(background="#d9d9d9")
        self.mode.configure(disabledforeground="#a3a3a3")
        self.mode.configure(foreground="#000000")
        self.mode.configure(text='''MODE''')

        self.og = tk.Label(self.main)
        self.og.place(relx=0.55, rely=0.567, height=26, width=42)
        self.og.configure(background="#d9d9d9")
        self.og.configure(disabledforeground="#a3a3a3")
        self.og.configure(foreground="#000000")
        self.og.configure(text='''OG''')

        self.ostacolo = tk.Button(self.main)
        self.ostacolo.place(relx=0.425, rely=0.68, height=24, width=75)
        self.ostacolo.configure(activebackground="#ececec")
        self.ostacolo.configure(activeforeground="#000000")
        self.ostacolo.configure(background="#d9d9d9")
        self.ostacolo.configure(disabledforeground="#a3a3a3")
        self.ostacolo.configure(foreground="#000000")
        self.ostacolo.configure(highlightbackground="#d9d9d9")
        self.ostacolo.configure(highlightcolor="black")
        self.ostacolo.configure(pady="0")
        self.ostacolo.configure(text='''OSTACOLO''')
        self.ostacolo.configure(command=self.entostacolo)

        self.stanza = tk.Button(self.main)
        self.stanza.place(relx=0.425, rely=0.771, height=24, width=75)
        self.stanza.configure(activebackground="#ececec")
        self.stanza.configure(activeforeground="#000000")
        self.stanza.configure(background="#d9d9d9")
        self.stanza.configure(disabledforeground="#a3a3a3")
        self.stanza.configure(foreground="#000000")
        self.stanza.configure(highlightbackground="#d9d9d9")
        self.stanza.configure(highlightcolor="black")
        self.stanza.configure(pady="0")
        self.stanza.configure(text='''STANZA''')
        self.stanza.configure(command= self.entstanza)

        self.stop = tk.Button(self.main)
        self.stop.place(relx=0.6, rely=0.885, height=24, width=47)
        self.stop.configure(activebackground="#ff0000")
        self.stop.configure(activeforeground="white")
        self.stop.configure(activeforeground="#000000")
        self.stop.configure(background="#ff0000")
        self.stop.configure(disabledforeground="#a3a3a3")
        self.stop.configure(foreground="#000000")
        self.stop.configure(highlightbackground="#d9d9d9")
        self.stop.configure(highlightcolor="black")
        self.stop.configure(pady="0")
        self.stop.configure(text='''STOP''')
        self.stop.configure(command=self.StopTotale)

        self.scala_velocita = tk.Scale(self.main, from_=0, to=100)
        self.scala_velocita.place(relx=0.315, rely=0.08, relwidth=0.345, relheight=0.0, height=51, bordermode='ignore')
        self.scala_velocita.configure(activebackground="#ececec")
        self.scala_velocita.configure(background="#d9d9d9")
        self.scala_velocita.configure(foreground="#000000")
        self.scala_velocita.configure(highlightbackground="#d9d9d9")
        self.scala_velocita.configure(highlightcolor="black")
        self.scala_velocita.configure(orient="horizontal")
        self.scala_velocita.configure(troughcolor="#d9d9d9")
        self.scala_velocita.set(variabili.vel)

        self.scala_avc = tk.Scale(self.main, from_=0, to=100)
        self.scala_avc.place(relx=0.315, rely=0.306, relwidth=0.345, relheight=0.0, height=52, bordermode='ignore')
        self.scala_avc.configure(activebackground="#ececec")
        self.scala_avc.configure(background="#d9d9d9")
        self.scala_avc.configure(foreground="#000000")
        self.scala_avc.configure(highlightbackground="#d9d9d9")
        self.scala_avc.configure(highlightcolor="black")
        self.scala_avc.configure(orient="horizontal")
        self.scala_avc.configure(troughcolor="#d9d9d9")
        self.scala_avc.set(variabili.avc)

        self.velocita = tk.Label(self.main)
        self.velocita.place(relx=0.415, rely=0.027, height=26, width=90)
        self.velocita.configure(background="#d9d9d9")
        self.velocita.configure(disabledforeground="#a3a3a3")
        self.velocita.configure(foreground="#000000")
        self.velocita.configure(text='''VELOCITA''')

        self.avc = tk.Label(self.main)
        self.avc.place(relx=0.415, rely=0.249, height=26, width=90)
        self.avc.configure(activebackground="#f9f9f9")
        self.avc.configure(activeforeground="black")
        self.avc.configure(background="#d9d9d9")
        self.avc.configure(disabledforeground="#a3a3a3")
        self.avc.configure(foreground="#000000")
        self.avc.configure(highlightbackground="#d9d9d9")
        self.avc.configure(highlightcolor="black")
        self.avc.configure(text='''AVC''')

        self.camera = tk.Label(self.main)
        self.camera.place(relx=0.435, rely=0.5, height=21, width=64)
        self.camera.configure(background="#d9d9d9")
        self.camera.configure(disabledforeground="#a3a3a3")
        self.camera.configure(foreground="#000000")
        self.camera.configure(text='''CAMERA''')



    def StanzaPage(self,top = None):

        self.stanza = tk.Frame(top)
        self.stanza.place(relx=0.01, rely=0.01, relheight=0.98, relwidth=0.98)
        self.stanza.configure(relief='groove')
        self.stanza.configure(borderwidth="2")
        self.stanza.configure(relief="groove")
        self.stanza.configure(background="#d9d9d9")

        load = Image.open("immagine.png")
        load = load.resize((300,150),Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
            
        self.ins = tk.Label(self.stanza,image = render,bd=0)
        self.ins.image = render
        self.ins.place(relx=0.25, rely=0.3, height=150, width=300)
        self.ins.configure(background ='#d9d9d9')
        self.ins.configure(highlightthickness =0)

        self.BS = tk.Button(self.stanza)
        self.BS.place(relx=0.27, rely=0.64, height=24, width=47)
        self.BS.configure(activebackground="#ececec")
        self.BS.configure(activeforeground="#000000")
        self.BS.configure(background="#ffff00")
        self.BS.configure(disabledforeground="#a3a3a3")
        self.BS.configure(foreground="#000000")
        self.BS.configure(highlightbackground="#d9d9d9")
        self.BS.configure(highlightcolor="black")
        self.BS.configure(pady="0")
        self.BS.configure(text='''BS''')
        self.BS.configure(command=self.basso_sinistra)

        self.BD = tk.Button(self.stanza)
        self.BD.place(relx=0.663, rely=0.64, height=24, width=47)
        self.BD.configure(activebackground="#ececec")
        self.BD.configure(activeforeground="#000000")
        self.BD.configure(background="#ffff00")
        self.BD.configure(disabledforeground="#a3a3a3")
        self.BD.configure(foreground="#000000")
        self.BD.configure(highlightbackground="#d9d9d9")
        self.BD.configure(highlightcolor="black")
        self.BD.configure(pady="0")
        self.BD.configure(text='''BD''')
        self.BD.configure(command=self.basso_destra)

        self.D = tk.Button(self.stanza)
        self.D.place(relx=0.78, rely=0.431, height=24, width=47)
        self.D.configure(activebackground="#ececec")
        self.D.configure(activeforeground="#000000")
        self.D.configure(background="#ffff00")
        self.D.configure(disabledforeground="#a3a3a3")
        self.D.configure(foreground="#000000")
        self.D.configure(highlightbackground="#d9d9d9")
        self.D.configure(highlightcolor="black")
        self.D.configure(pady="0")
        self.D.configure(text='''D''')
        self.D.configure(command=self.destra)

        self.AD = tk.Button(self.stanza)
        self.AD.place(relx=0.663, rely=0.249, height=24, width=47)
        self.AD.configure(activebackground="#ececec")
        self.AD.configure(activeforeground="#000000")
        self.AD.configure(background="#ffff00")
        self.AD.configure(disabledforeground="#a3a3a3")
        self.AD.configure(foreground="#000000")
        self.AD.configure(highlightbackground="#d9d9d9")
        self.AD.configure(highlightcolor="black")
        self.AD.configure(pady="0")
        self.AD.configure(text='''AD''')
        self.AD.configure(command=self.avanti_destra)

        self.A = tk.Button(self.stanza)
        self.A.place(relx=0.4625, rely=0.249, height=24, width=47)
        self.A.configure(activebackground="#ececec")
        self.A.configure(activeforeground="#000000")
        self.A.configure(background="#ffff00")
        self.A.configure(disabledforeground="#a3a3a3")
        self.A.configure(foreground="#000000")
        self.A.configure(highlightbackground="#d9d9d9")
        self.A.configure(highlightcolor="black")
        self.A.configure(pady="0")
        self.A.configure(text='''A''')
        self.A.configure(command=self.avanti)

        self.AS = tk.Button(self.stanza)
        self.AS.place(relx=0.27, rely=0.249, height=24, width=47)
        self.AS.configure(activebackground="#ececec")
        self.AS.configure(activeforeground="#000000")
        self.AS.configure(background="#ffff00")
        self.AS.configure(disabledforeground="#a3a3a3")
        self.AS.configure(foreground="#000000")
        self.AS.configure(highlightbackground="#d9d9d9")
        self.AS.configure(highlightcolor="black")
        self.AS.configure(pady="0")
        self.AS.configure(text='''AS''')
        self.AS.configure(command=self.avanti_sinistra)

        self.S = tk.Button(self.stanza)
        self.S.place(relx=0.15, rely=0.431, height=24, width=47)
        self.S.configure(activebackground="#ececec")
        self.S.configure(activeforeground="#000000")
        self.S.configure(background="#ffff00")
        self.S.configure(disabledforeground="#a3a3a3")
        self.S.configure(foreground="#000000")
        self.S.configure(highlightbackground="#d9d9d9")
        self.S.configure(highlightcolor="black")
        self.S.configure(pady="0")
        self.S.configure(text='''S''')
        self.S.configure(command=self.sinistra)

        self.Scale1 = ttk.Scale(self.stanza, from_=0, to=1)
        self.Scale1.place(relx=0.425, rely=0.068, relwidth=0.17, relheight=0.0, height=26, bordermode='ignore')
        self.Scale1.set(variabili.stanza_mode)

        self.manuale = tk.Label(self.stanza)
        self.manuale.place(relx=0.25, rely=0.068, height=21, width=64)
        self.manuale.configure(background="#d9d9d9")
        self.manuale.configure(disabledforeground="#a3a3a3")
        self.manuale.configure(foreground="#000000")
        self.manuale.configure(text='''MANUALE''')

        self.auto = tk.Label(self.stanza)
        self.auto.place(relx=0.663, rely=0.068, height=21, width=44)
        self.auto.configure(activebackground="#f9f9f9")
        self.auto.configure(activeforeground="black")
        self.auto.configure(background="#d9d9d9")
        self.auto.configure(disabledforeground="#a3a3a3")
        self.auto.configure(foreground="#000000")
        self.auto.configure(highlightbackground="#d9d9d9")
        self.auto.configure(highlightcolor="black")
        self.auto.configure(text='''AUTO''')

        self.salva = tk.Button(self.stanza)
        self.salva.place(relx=0.34, rely=0.794, height=24, width=47)
        self.salva.configure(activebackground="#ececec")
        self.salva.configure(activeforeground="#000000")
        self.salva.configure(background="#00ff00")
        self.salva.configure(disabledforeground="#a3a3a3")
        self.salva.configure(foreground="#000000")
        self.salva.configure(highlightbackground="#d9d9d9")
        self.salva.configure(highlightcolor="black")
        self.salva.configure(pady="0")
        self.salva.configure(text='''salva''')
        self.salva.configure(command=self.SalvaStanza)

        self.back = tk.Button(self.stanza)
        self.back.place(relx=0.595, rely=0.794, height=24, width=47)
        self.back.configure(activebackground="#ececec")
        self.back.configure(activeforeground="#000000")
        self.back.configure(background="#ff0000")
        self.back.configure(disabledforeground="#a3a3a3")
        self.back.configure(foreground="#000000")
        self.back.configure(highlightbackground="#d9d9d9")
        self.back.configure(highlightcolor="black")
        self.back.configure(pady="0")
        self.back.configure(text='''back''')
        self.back.configure(command= self.exstanza)


    def OstacoloPage(self,top = None):
        self.FrameOstacolo = tk.Frame(top)
        self.FrameOstacolo.place(relx=0.01, rely=0.01, relheight=0.98, relwidth=0.98)
        self.FrameOstacolo.configure(relief='groove')
        self.FrameOstacolo.configure(borderwidth="2")
        self.FrameOstacolo.configure(relief="groove")
        self.FrameOstacolo.configure(background="#d9d9d9")

        self.mode = ttk.Scale(self.FrameOstacolo, from_=0, to=1.0)
        self.mode.place(relx=0.408, rely=0.295, relwidth=0.17, relheight=0.0, height=26, bordermode='ignore')
        self.mode.set(variabili.ostacolo_mode)

        self.angolo = ttk.Scale(self.FrameOstacolo, from_=0, to=1.0)
        self.angolo.place(relx=0.408, rely=0.408, relwidth=0.17, relheight=0.0, height=26, bordermode='ignore')
        self.angolo.set(variabili.ostacolo_angolo)

        self.direzione = ttk.Scale(self.FrameOstacolo, from_=0, to=1.0)
        self.direzione.place(relx=0.408, rely=0.522, relwidth=0.17, relheight=0.0, height=26, bordermode='ignore')
        self.direzione.set(variabili.ostacolo_direzione)

        self.salva = tk.Button(self.FrameOstacolo)
        self.salva.place(relx=0.323, rely=0.794, height=24, width=38)
        self.salva.configure(activebackground="#ececec")
        self.salva.configure(activeforeground="#000000")
        self.salva.configure(background="#00ff00")
        self.salva.configure(disabledforeground="#a3a3a3")
        self.salva.configure(foreground="#000000")
        self.salva.configure(highlightbackground="#d9d9d9")
        self.salva.configure(highlightcolor="black")
        self.salva.configure(pady="0")
        self.salva.configure(text='''Salva''')
        self.salva.configure(command=self.SalvaOstacolo)

        self.back = tk.Button(self.FrameOstacolo)
        self.back.place(relx=0.595, rely=0.794, height=24, width=47)
        self.back.configure(activebackground="#ececec")
        self.back.configure(activeforeground="#000000")
        self.back.configure(background="#ff0000")
        self.back.configure(disabledforeground="#a3a3a3")
        self.back.configure(foreground="#000000")
        self.back.configure(highlightbackground="#d9d9d9")
        self.back.configure(highlightcolor="black")
        self.back.configure(pady="0")
        self.back.configure(text='''back''')
        self.back.configure(command=self.exostacolo)

        self.auto = tk.Label(self.FrameOstacolo)
        self.auto.place(relx=0.20, rely=0.295, height=21, width=38)
        self.auto.configure(background="#d9d9d9")
        self.auto.configure(disabledforeground="#a3a3a3")
        self.auto.configure(foreground="#000000")
        self.auto.configure(text='''AUTO''')

        self.g_90 = tk.Label(self.FrameOstacolo)
        self.g_90.place(relx=0.204, rely=0.408, height=21, width=34)
        self.g_90.configure(activebackground="#f9f9f9")
        self.g_90.configure(activeforeground="black")
        self.g_90.configure(background="#d9d9d9")
        self.g_90.configure(disabledforeground="#a3a3a3")
        self.g_90.configure(foreground="#000000")
        self.g_90.configure(highlightbackground="#d9d9d9")
        self.g_90.configure(highlightcolor="black")
        self.g_90.configure(text='''90°''')

        self.g_180 = tk.Label(self.FrameOstacolo)
        self.g_180.place(relx=0.68, rely=0.408, height=21, width=34)
        self.g_180.configure(activebackground="#f9f9f9")
        self.g_180.configure(activeforeground="black")
        self.g_180.configure(background="#d9d9d9")
        self.g_180.configure(disabledforeground="#a3a3a3")
        self.g_180.configure(foreground="#000000")
        self.g_180.configure(highlightbackground="#d9d9d9")
        self.g_180.configure(highlightcolor="black")
        self.g_180.configure(text='''180°''')

        self.sinistraa = tk.Label(self.FrameOstacolo)
        self.sinistraa.place(relx=0.187, rely=0.522, height=21, width=64)
        self.sinistraa.configure(activebackground="#f9f9f9")
        self.sinistraa.configure(activeforeground="black")
        self.sinistraa.configure(background="#d9d9d9")
        self.sinistraa.configure(disabledforeground="#a3a3a3")
        self.sinistraa.configure(foreground="#000000")
        self.sinistraa.configure(highlightbackground="#d9d9d9")
        self.sinistraa.configure(highlightcolor="black")
        self.sinistraa.configure(text='''SINISTRA''')

        self.destraa = tk.Label(self.FrameOstacolo)
        self.destraa.place(relx=0.663, rely=0.522, height=21, width=64)
        self.destraa.configure(activebackground="#f9f9f9")
        self.destraa.configure(activeforeground="black")
        self.destraa.configure(background="#d9d9d9")
        self.destraa.configure(disabledforeground="#a3a3a3")
        self.destraa.configure(foreground="#000000")
        self.destraa.configure(highlightbackground="#d9d9d9")
        self.destraa.configure(highlightcolor="black")
        self.destraa.configure(text='''DESTRA''')

        self.guidato = tk.Label(self.FrameOstacolo)
        self.guidato.place(relx=0.67, rely=0.295, height=21, width=60)
        self.guidato.configure(activebackground="#f9f9f9")
        self.guidato.configure(activeforeground="black")
        self.guidato.configure(background="#d9d9d9")
        self.guidato.configure(disabledforeground="#a3a3a3")
        self.guidato.configure(foreground="#000000")
        self.guidato.configure(highlightbackground="#d9d9d9")
        self.guidato.configure(highlightcolor="black")
        self.guidato.configure(text='''GUIDATO''')


    def entostacolo(self):
        self.main.destroy()
        self.OstacoloPage()
    def exostacolo(self):
        self.FrameOstacolo.destroy()
        print('OSTACOLO---------')
        print(variabili.ostacolo_mode)
        print(variabili.ostacolo_angolo)
        print(variabili.ostacolo_direzione)
        self.MainPage()



    def entstanza(self):
        self.main.destroy()
        self.StanzaPage()
    def exstanza(self):
        self.stanza.destroy()
        print('STANZA-----------')        
        print(variabili.stanza_mode)
        print(variabili.stanza_uscita)
        self.MainPage()

    '''''''''''''''COMANDI MAIN'''''''''''''''
  
    def SalvaTutto(self):
        variabili.avc = int(self.scala_avc.get())
        variabili.vel = int(self.scala_velocita.get())
        variabili.camera_mode = int(self.camera_scale.get())

        np.savetxt("variabili/avc.txt", [variabili.avc], fmt='%1i', delimiter='\t')
        np.savetxt("variabili/vel.txt", [variabili.vel], fmt='%1i', delimiter='\t')
        np.savetxt("variabili/camera_mode.txt", [variabili.camera_mode], fmt='%1i', delimiter='\t')
        


        return
    def StopTotale(self):
        print('----------------')
        print('------STOP------')
        print('----------------')
        #Immettere le Variabili nel file

        variabili.vel=0

        main_support.destroy_window()

    
    '''''''''''''''COMANDI STANZA'''''''''''''''
    def avanti(self):
        variabili.nuova_uscita='avanti'
        return
    def avanti_destra(self):
        variabili.nuova_uscita='avant_idestra'
        return
    def avanti_sinistra(self):
        variabili.nuova_uscita='avanti_sinistra'
        return
    def destra(self):
        variabili.nuova_uscita='destra'
        return
    def sinistra(self):
        variabili.nuova_uscita='sinistra'
        return
    def basso_destra(self):
        variabili.nuova_uscita='basso_destra'
        return
    def basso_sinistra(self):
        variabili.nuova_uscita='basso_sinistra'
        return

    def SalvaStanza(self):
        variabili.stanza_uscita=variabili.nuova_uscita
        variabili.stanza_mode = int(self.Scale1.get())

        np.savetxt("variabili/stanza_mode.txt", [variabili.stanza_mode], fmt='%1i', delimiter='\t')
        np.savetxt("variabili/stanza_uscita.txt",np.array(variabili.stanza_uscita.split(" ")),fmt="%s", delimiter=" " )
        

        return
    '''''''''''''''COMANDI OSTACOLO'''''''''''''''
    def SalvaOstacolo(self):
        variabili.ostacolo_mode = int(self.mode.get())
        variabili.ostacolo_angolo = int(self.angolo.get())
        variabili.ostacolo_direzione = int(self.direzione.get())

        np.savetxt("variabili/ostacolo_mode.txt", [variabili.ostacolo_mode], fmt='%1i', delimiter='\t')
        np.savetxt("variabili/ostacolo_angolo.txt", [variabili.ostacolo_angolo], fmt='%1i', delimiter='\t')
        np.savetxt("variabili/ostacolo_direzione.txt", [variabili.ostacolo_direzione], fmt='%1i', delimiter='\t')
        #print(type(variabili))

        return

def startPage():
    t1=Thread(target=vp_start_gui , args=())
    t1.start()


if __name__ == '__main__':

    #t1=Thread(target=f,args=())
    #t1.start()
    vp_start_gui()






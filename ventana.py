from Tkinter import *
from tkFileDialog   import askopenfilename
import os
import commands

def NewFile():
    print "New File!"
def OpenFile():
    name = askopenfilename()
    print name
def About():
    print "This is a simple example of a menu"
    
def listar(event):
    print("Listar bots")
def iniciar(event):
    print("Iniciar") 
    result=commands.getoutput('/usr/bin/python pruebatw.py')
def quit(event):                           
    print("Saliendo del programa...") 
    import sys; sys.exit() 

def abrirventana2(event):
    win=Tk()
    win.geometry('500x300+700+100')


root = Tk()
root.geometry('500x300+150+100')
root.title("BOTNET SEGURIDAD")
root.configure(background="grey")


w = Label(root, text="MENU PRINCIPAL", bg="blue", fg="white")
w.pack(fill=X)



boton1 = Button(None, text='Listar BOTS')
boton1.pack(fill=BOTH)
boton1.bind('<Button-1>', abrirventana2)
boton2 = Button(None, text='INICIAR')
boton2.pack(fill=BOTH)
boton2.bind('<Button-1>', iniciar)
boton3 = Button(None, text='Salir')
boton3.pack(fill=BOTH)
boton3.bind('<Button-1>', quit)
mainloop()
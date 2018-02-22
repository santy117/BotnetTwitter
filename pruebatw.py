import time
from threading import Thread
import tweepy
import commands



#Twitter API credentials   NUEVAS
_CONSUMER_KEY = "RDLCb666OV6vpCd2Io0efsrMQ"
_CONSUMER_SECRET = "xp4bFkSrOUbPmDHvyBxXeHRw3w1DGxPjzgnN7FnbqS482gs5TQ"
_ACCESS_KEY = "936178099078750208-jXFXv9IAKPY77BlN14K9LeX5x1FjW6L"
_ACCESS_SECRET = "YFg0VwPPvBOS5FAFNIY8RA34Cxe9XODljTYeQwddtOmrH"


AUTH = tweepy.OAuthHandler(_CONSUMER_KEY, _CONSUMER_SECRET)
AUTH.set_access_token(_ACCESS_KEY, _ACCESS_SECRET)
AUTH.secure = True
API = tweepy.API(AUTH)

#UPDATE STATUS
SEARCH_TEXT = "#FFFJJJGGG69jeje"
SEARCH_NUMBER = 2
SEARCH_RESULT = API.search(SEARCH_TEXT, rpp=SEARCH_NUMBER)


def timer():
    count = 0
    while True:
        time.sleep(10)
        count += 1  
        ejecucion()  
                
repeticion=0
background_thread = Thread(target=timer)
background_thread.start()

def ejecucion():
    global repeticion
    COUNTER = 0
    if repeticion == "iniciar":
        print "Sin nuevos cambios, seguimos con el programa iniciado."
    elif repeticion == "parar":
        print "Sin nuevos cambios, seguimos con el programa parado."  
    if SEARCH_RESULT > 0:
        for i in SEARCH_RESULT:
            COUNTER = COUNTER + 1
            if COUNTER == 1:
                X = i.text
                Y, Z = X.split("#FFFJJJGGG69jeje")
                H,L = Z.split("///")
                H = H.strip()
        if H == "iniciar" and repeticion != "iniciar":
            print ("Se ha seleccionado iniciar el programa a la pagina: "+L.strip())
            #no va commands.getoutput, probar con subprocess
            repeticion = "iniciar"
        if H == "parar" and repeticion != "parar":
            print "Se ha seleccionado parar el programa."
            repeticion = "parar"
    else:
        print "Sin ninguna orden por el momento..."


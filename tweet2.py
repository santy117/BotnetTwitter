import tweepy
import json

# Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time

# Variables that contains the user credentials to access Twitter API 
consumer_key = "3ncn0B0h8rLQWXQXTOFRYUIyX"
consumer_secret = "NhxmLrk5Upz9te7zXEgbBcjAPJeNCVxMZzad7VbfQznHxhHsno"
access_token = "936178099078750208-Ru6DwsYwl3vZ68LVhU3AoFnJtsFK4eK"
access_token_secret = "SdvMznJrj4zLeWV2BXboetwh2e7iA44XkshUBd4lvOwwV"

# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        tweet = data.split("#FFFJJJGGG69jeje")[1].split('","source')[0]
        print tweet
        H,L = tweet.split("PROGRAMA")
        H = H.strip()
        L = L.strip()
        if H == "iniciar":
            print ("Se ha seleccionado iniciar el programa a la pagina: "+L.strip())
        if H == "parar":
            print "Se ha seleccionado parar el programa."
        return True

    def on_error(self, status):
        if status == 420:
            #returning False in on_data disconnects the stream
            print "Excedido numero de accesos por tiempo, debes esperar un tiempo.Durmiendo el programa 900 segundos"
            time.sleep(900)
       


if __name__ == '__main__':
    # This handles Twitter authentication and connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=["#FFFJJJGGG69jeje"])

import spotipy
import os
import psycopg2
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

idx = 0
n = 0
m = 0
found = False

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPE = 'user-library-read'

DATABASE = os.getenv("DATABASE")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET,
    redirect_uri = REDIRECT_URI,
    scope=SCOPE
))

def GetLikedSongs(limit,offset):
    global m
    global found

    results = sp.current_user_saved_tracks(limit,offset,)
    for idx, item in enumerate(results['items']):
        track = item['track']

        Name = track['name'].replace("'"," ")
        Artist = track['artists'][0]['name'].replace("'"," ")
        Album = track['album']['name'].replace("'"," ")
        Date = item['added_at'][0:4]+item['added_at'][5:7]+item['added_at'][8:10]
        Id = item['track']['id']

        print(f"{m + 1}. {Name} - {Artist} - {Album} - {Date} - {Id}")
        
        if (FetchDatabase(Id) == 0 ):

            InsertDatabase(Name,Artist,Album,Date,Id)

        else:
            found = True
            return(found)

        m += 1
        
def Total():
    results = sp.current_user_saved_tracks(limit = 1)
    total = results['total']
    return total

def FetchDatabase(Id):
    connection = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    cursor = connection.cursor()
    
    cursor.execute("SELECT * from musicsaver where Id = " + "'" + Id + "'")

    record = cursor.fetchall()

    return(len(record))

def InsertDatabase(Track,Artist,Album,Date,Id):
    connection = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    cursor = connection.cursor()
    
    cursor.execute("INSERT INTO musicsaver (track,artist,album,date,id) VALUES (" + "'" + Track + "'," + "'" + Artist + "'," + "'" + Album + "'," + "'" + Date + "'," + "'" + Id + "'" + ")" )

    connection.commit()


def Main():
    global n
    global found

    while n < Total():
        GetLikedSongs(limit = 50,offset = n)

        if found == True:
            return

        n += 50

if __name__=="__main__":
    Main()

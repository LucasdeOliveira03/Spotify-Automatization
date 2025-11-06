from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import os
import sqlite3
import datetime

# Used variables
idx = 0
n = 0
m = 0
found = False
con = sqlite3.connect("musicdb.db")
cur = con.cursor()

table = "musicsaver" # Name your table
playlist_id = "6OQdpxRYAHCpwJ3C6JmdIj" # Name your playlist


load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPE = 'user-library-read'

# Connect spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET,
    redirect_uri = REDIRECT_URI,
    scope = SCOPE
))

def CreateTable(table):
    cur.execute(f"""
                CREATE TABLE {table}(
                id TEXT, 
                track TEXT, 
                artist TEXT, 
                album TEXT, 
                date TEXT,
                runtime TEXT,
                plussy TEXT) 
                """)

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
        date = datetime.datetime.now()
        RunTime = date.strftime("%Y%m%d_%X")
        

        print(f"{m + 1}. {Name} - {Artist} - {Album} - {Date} - {Id} - {RunTime}")
        
        if (CompareDatabase(Id) == 0 ):

            InsertDatabase(Name,Artist,Album,Date,Id,RunTime)

        else:
            found = True
            return(found)

        m += 1
        
def Total():
    results = sp.current_user_saved_tracks(limit = 1)
    total = results['total']
    return total

def CompareDatabase(Id):
    cur.execute(f"""
                SELECT * 
                FROM {table} 
                WHERE Id = '{Id}'
                """)

    record = cur.fetchall()

    return(len(record))

def InsertDatabase(Track,Artist,Album,Date,Id,RunTime):
    cur.execute(f"""
                INSERT INTO {table} (id,track,artist,album,date,runtime)
                VALUES('{Id}','{Track}','{Artist}','{Album}','{Date}','{RunTime}')
                """)
    
    con.commit()

def FetchDatabase():
    cur.execute(f"""
                SELECT *
                FROM {table}
                WHERE plussy IS NULL
                """)

    record = cur.fetchall()

    return(record)

def TrackUsed(Id):
    cur.execute(f"""
                UPDATE {table}
                SET plussy = '*'
                WHERE id = '{Id}'
                """)
    
    con.commit()

def Main():
    global n
    global found

    # Create table if doesn't exist
    cur.execute(f"""
                SELECT name 
                FROM sqlite_master 
                WHERE type='table' AND name='{table}'
                """)

    if cur.fetchone():
        print(f"the table '{table}' already exist")

    else:
        print(f"creating table '{table}'")

        CreateTable(table)
        
        print(f"table '{table}' created")

    # I can't remember how but it loops through all liked songs
    while n < Total():
        GetLikedSongs(limit = 50,offset = n)

        if found == True:
            break

        n += 50

    # Insert tracks into the playlist
    record = FetchDatabase()

    for track in record:
        Id = track[0]
        Track = track[1]

        print(f"id = {Id} track = {Track}")
        sp.playlist_add_items(playlist_id,[Id])

        TrackUsed(Id)    

if __name__=="__main__":
    Main()

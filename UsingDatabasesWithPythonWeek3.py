import sqlite3
import xml.etree.ElementTree as ET

conn = sqlite3.connect("trackdb.sqlite") #The SQL thing you are creating
cur = conn.cursor() #setting a cursor so now it can execute commands

#Executes a whole script
#DROP TABLE clears the tables if they exist there
#Create table creates tables with an id and name and artist_ids
#the id INTEGER NOT NULL... represents the primary keys
#The album_id INTEGER and artist_id INTEGER represents the foreign keys
#The len INTEGER, rating INTEGER, and count INTEGER represents the other
#characteristics tagged on

cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS ALBUM;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS TRACK;

CREATE TABLE ARTIST(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);  

CREATE TABLE Genre(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE ALBUM(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE TRACK(
    id INTEGER NOT NULL PRIMARY KEY
        AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE,
    album_id INTEGER,
    genre_id INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);

''')
def lookup(d, key): #A function used to check if "Name" or "Artist" ...
    #are in the XML thing u are searching in
    found = False
    for child in d:
        if found : return child.text
        if child.tag == 'key' and child.text == key :
            found = True
    return None
filename = input("Enter the file name: ")

if (len(filename) < 1):
    filename = "Library.xml"

XMlparsed = ET.parse(filename) #parses the file into a sort of Tree where u
#dig down it
findall = XMlparsed.findall("dict/dict/dict") #finds all dict/dict/dict keys
#and pairs and stores it in dictionary findall where u dig stuff thru
print("Dict count:", len(findall)) #shows how many pairs are counted
for every in findall:
    if (lookup(every,"Track ID") is None) : continue
    name = lookup(every, 'Name')
    artist = lookup(every, 'Artist')
    genre = lookup(every, 'Genre')
    album = lookup(every, 'Album')
    count = lookup(every, 'Play Count')
    rating = lookup(every, 'Rating')
    length = lookup(every, 'Total Time')

    if name is None or artist is None or album is None or genre is None:
        continue #Some sanitiy checking
        #if this condition where to exist we just go on

    print(name, genre, artist, album, count, rating, length)

    cur.execute('''INSERT OR IGNORE INTO Artist (name) 
            VALUES ( ? )''', (artist,))
    #OR IGNORE is bc we put a constraint UNIQUE On it so it says
    #if its already there don't put it again in that same row
    cur.execute('SELECT id FROM Artist WHERE name = ? ', (artist,))
    artist_id = cur.fetchone()[0] #gets the artist id

    cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id) 
            VALUES ( ?, ? )''', (album, artist_id)) #sents in artist_id from ^
    cur.execute('SELECT id FROM Album WHERE title = ? ', (album,))
    album_id = cur.fetchone()[0]
    #you basically pass the key along
    #INSERT OR REPLACE MEAN IT WILL UPDATE if the unique constraint is violated
    #It turns into a update

    cur.execute('''INSERT OR REPLACE INTO Track
            (title, album_id, len, rating, count) 
            VALUES ( ?, ?, ?, ?, ? )''',
            (name, album_id, length, rating, count))

    cur.execute('''INSERT OR IGNORE INTO Genre (name) 
        VALUES ( ? )''', ( genre, ) )
    cur.execute('SELECT id FROM Genre WHERE name = ? ', (genre, ))
    genre_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Track
            (title, genre_id, album_id, len, rating, count) 
            VALUES ( ?, ?, ?, ?, ?, ? )''',
            (name,genre_id,album_id,length, rating, count))

    conn.commit()


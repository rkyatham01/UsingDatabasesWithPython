import json
import sqlite3

fileconnect = sqlite3.connect("rosterdb.sqlite")
cur = fileconnect.cursor() #sets a cursor so now its ready for executing sql commands

#Clears the tables everytime you reset
cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User(
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE Course(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title   TEXT UNIQUE
);

CREATE TABLE Member(
    user_id    INTEGER,
    course_id   INTEGER,
    role    INTEGER,
    PRIMARY KEY (user_id, course_id)
)
''')

filename = input("Enter file name")

if (len(filename) < 1):
    filename = "roster_data.json"

ArrayOfdata = open(filename).read()
jsondata = json.loads(ArrayOfdata)

for line in jsondata:

    name = line[0]
    title = line[1]
    role_id = line[2] #add the role id for the merged table

    print((name,title))

    cur.execute('''INSERT OR IGNORE INTO User (name)
    VALUES ( ? )''', ( name, ) )
    cur.execute('SELECT id FROM User WHERE name = ? ', (name, ))
    user_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Course (title)
        VALUES ( ? )''', (title, ) )
    cur.execute('SELECT id FROM Course WHERE title = ? ', (title, ))
    course_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Member
        (user_id, course_id, role) VALUES ( ?, ?, ?)''',
        ( user_id, course_id, role_id ) ) #combined it here

    fileconnect.commit()
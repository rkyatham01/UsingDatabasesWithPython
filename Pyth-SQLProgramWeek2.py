import sqlite3 #import SQLITE

connection = sqlite3.connect("emaildb.sqlite") #creates a emaildb sqlite file and connects it to connection

curr = connection.cursor() #Kind of like a file handler which basically puts a cursor in the SQL

curr.execute("DROP TABLE IF EXISTS Counts") #Deletes table if already there so you never repeat

curr.execute('''CREATE TABLE Counts (org TEXT, count INTEGER)''')

filename = input("Enter file name :")
if (len(filename) < 1):
    filename = "mbox.txt"

filehndlr = open(filename)
var = ""

for line in filehndlr:
    line = line.rstrip()
    if line.startswith("From: "):
        line = line.split()
        email = line[1] #emails are in var
        var = email.split("@")[1]
        curr.execute("SELECT count FROM Counts WHERE org = ?",(var,)) #Selects count as a sort of a pointer of where to update
        #when email = var , has to be in tuple format for some reason
        #? is a sort of place holder for the email
        row = curr.fetchone() #After finding the email it gets the info of the email
        if row is None:
            curr.execute("INSERT INTO Counts (org,count) VALUES (?,1)",(var,)) #same format so if row is None then
        #it inserts a new thing into the table
        else:
            curr.execute("UPDATE Counts SET count = count + 1 WHERE org = ?", (var,))

    connection.commit()

sqlstring = "SELECT org, count FROM Counts ORDER BY count DESC LIMIT 1" #Orders the sqlstring by count
    #gets only top 1
for row in curr.execute((sqlstring)):
    print(str(row[0]), row[1])

curr.close()



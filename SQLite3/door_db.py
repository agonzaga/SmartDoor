import sqlite3
import os

def open_db():
    global conn
    global c
    conn = sqlite3.connect('photo_collection.db')
    c = conn.cursor()

def create_table():
    c.execute('''CREATE TABLE photos (Name label, Link path);''')

def insert(file_name, data_path):
    # Insert a row of data (name, photo)
    c.execute('''INSERT INTO photos (Name, Link) VALUES (?,?)''', (file_name, data_path))
    #c.execute('''INSERT INTO photos (Name, Link) VALUES ("hello", "no")''')

def close_db():
    # Committing the changes
    conn.commit()
    conn.close()

def main():
    open_db()
    # create_table()
    try:
        create_table()
    except:
        pass
    # insert("andre", "/sada")
    get_db()
    close_db()

# get dict of lists from db. {david: [image1, image2]}
def get_db():
    #connect database
    db = sqlite3.connect(db_name)

    cursor = db.cursor()

    # SQL query in command
    command = '''SELECT *
        FROM Photos;'''

    # execute command
    cursor.execute(command)

    mydict = {}

    for row in cursor:
        key = row[0]
        image_path = row[1]
        mydict[key] = image_path
        if key in mydict:
            mydict[key].append(image_path)
        else:
            mydict[key] = [image_path]

    db.commit()
    db.close()


if __name__ == '__main__':
    main()
import sqlite3

def create_table():
    c.execute("CREATE TABLE photos (Name name)")

def open_db():
    global conn
    global c
    conn = sqlite3.connect('photo_collection.db')
    c = conn.cursor()

def insert():
    # Insert a row of data (name, photo)
    c.execute("INSERT INTO photos (Name) values ?")

def close_db():
    # Committing the changes
    conn.commit()
    conn.close()

def main():
    open_db()

if __name__ == '__main__':
    main()
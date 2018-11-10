import sqlite3

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
    insert("nameis", "path")
    close_db()

if __name__ == '__main__':
    main()
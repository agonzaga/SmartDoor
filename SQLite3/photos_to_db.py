import sqlite3
import os
import sys
from os.path import basename

fileList = {}

def readInFiles(basepath):
    if not os.path.isdir(basepath):
        raise Exception("provided path must be a directory.")
    for filename in os.listdir(basepath):
        fullpath = os.path.join(basepath, filename)
        print("Looking at", fullpath)
        if os.path.isdir(fullpath):
            print("descending into", filename)
            readInFiles(fullpath)
        elif filename.endswith(".jpg"):
            name = os.path.basename(os.path.dirname(fullpath))
            if(name not in fileList):
                fileList[name] = []
                fileList[name].append(os.path.abspath(fullpath))
            else:   # means the person already exists
                fileList[name].append(os.path.abspath(fullpath))
        else:
            print("not a jpg, skipping", filename)

def error():
        print("Not enough arguments!")

def open_db():
    global conn
    global c
    conn = sqlite3.connect('photo_collection.db')
    c = conn.cursor()

def create_table():
    c.execute('''CREATE TABLE photos (Name label, Link path);''')

def insert(file_name, data_path):
    # Insert a row of data (name, full paths)
    c.execute('''INSERT INTO photos (Name, Link) VALUES (?,?)''', (file_name, data_path))

# Pass in the dictionary: {Name1 : [path1, path2], Name2 : [path3, path4], ...}
def populate_db(file_dict):
    all_paths = ""
    # There is a unique path for each photo, the multiple paths produced from the multiple photos of the same person is stored as one entry in the SQL
    #   database. These different paths are separated by spaces.
    for k, v in file_dict.items():
        for paths in v:
            all_paths += paths + " "
        insert(k, all_paths[:-1])
        all_paths = ""

def close_db():
    # Committing the changes
    conn.commit()
    conn.close()

if __name__ == '__main__':
    def main():
        open_db()
        try:
            create_table()
        except:
            pass
        readInFiles(sys.argv[1])
        populate_db(fileList)
        close_db()

    if len(sys.argv) < 2:
        exit(error())
    else:
        main()

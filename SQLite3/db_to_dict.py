import sqlite3
import os
import sys
from os.path import basename

# get dict of lists from db. {david: [image1, image2]}
def get_db(db_name):
    #connect database
    db = sqlite3.connect(db_name)

    cursor = db.cursor()

    # SQL query in command
    command = '''SELECT * FROM Photos;'''

    # execute command
    cursor.execute(command)

    mydict = {}

    for row in cursor:
        key = row[0]
        image_path = row[1]
        if key in mydict:
            mydict[key].append(image_path)
        else:
            mydict[key] = [image_path]

    return mydict

    db.commit()
    db.close()

if __name__ == '__main__':
    def main():
        try:
            create_table()
        except:
            pass
        photo_dict = get_db("photo_collection.db")
        for k, v in photo_dict.items():
            print(k, v)
            print("\n")
        close_db()

    try:
        main()
    except:
        "Error occurred!"
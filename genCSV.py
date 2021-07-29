import sqlite3

def read_all(_table, _db):
    _cursor = _db.cursor()
    _ret = _cursor.execute(f"SELECT * FROM {_table}").fetchall()
    return _ret

if __name__ == "__main__":
    database = sqlite3.connect("./picture.db")
    with open("./bing.csv", "w") as f:
        for pic in read_all("bing", database):
            f.write(f"{pic[0]},{pic[1]},{pic[2]}\n")
    
    with open("./apod.csv", "w") as f:
        for pic in read_all("apod", database):
            f.write(f"{pic[0]},{pic[1]},{pic[2]}\n")
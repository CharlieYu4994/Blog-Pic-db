import sqlite3

def read_all(_db):
    _cursor = _db.cursor()
    _ret = _cursor.execute(f"SELECT * FROM bing").fetchall()
    return _ret

if __name__ == "__main__":
    database = sqlite3.connect("./picture.db")
    tmp = read_all(database)
    with open("./picture.csv", "w") as f:
        for pic in tmp:
            f.write(f"{pic[0]},{pic[1]},{pic[2]}\n")
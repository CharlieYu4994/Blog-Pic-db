import sqlite3, requests, json

def add_line(_date, _url, _db):
    _cursor = _db.cursor()
    _cursor.execute(f"""INSERT INTO bing (DATE, BURL) VALUES ('{_date}', '{_url}')""")
    _db.commit()

def chk_line(_date, _db):
    _cursor = _db.cursor()
    _cursor.execute(f"""SELECT IFNULL((SELECT DATE FROM bing WHERE DATE='{_date}'), "NULL")""")
    tmp = _cursor.fetchall()[0][0]
    return False if tmp == "NULL" else True

if __name__ == "__main__":
    database = sqlite3.connect('./picture.db')
    res = requests.get("https://cn.bing.com/HPImageArchive.aspx?format=js&idx=-1&n=9&mkt=zh-cn")
    tmp = json.loads(res.content.decode())["images"]
    for pic in tmp[::-1]:
        if not chk_line(pic["enddate"], database):
            add_line(pic["enddate"], pic["urlbase"], database)
        
    

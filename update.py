import sqlite3, requests, json, time
from lxml import etree

def add_line(_table, _date, _url, _db):
    _cursor = _db.cursor()
    _cursor.execute(f"""INSERT INTO {_table} (DATE, BURL) VALUES ('{_date}', '{_url}')""")
    _db.commit()

def chk_line(_table, _date, _db):
    _cursor = _db.cursor()
    _cursor.execute(f"""SELECT IFNULL((SELECT DATE FROM {_table} WHERE DATE='{_date}'), "NULL")""")
    tmp = _cursor.fetchone()[0]
    return False if tmp == "NULL" else True

def update_bing(_db):
    res = requests.get("https://cn.bing.com/HPImageArchive.aspx?format=js&idx=-1&n=9&mkt=zh-cn")
    tmp = json.loads(res.content.decode())["images"]
    for pic in tmp[::-1]:
        if not chk_line("bing", pic["enddate"], _db):
            add_line("bing", pic["enddate"], pic["urlbase"], _db)

def update_apod(_db):
    date = time.time()
    pics = list()

    for _ in range(5):
        date -= 3600*24
        tmp = time.strftime("%Y%m%d", time.localtime(date))

        resp = requests.get(f"https://apod.nasa.gov/apod/ap{tmp[2:]}.html")
        if resp.status_code != 200:
            continue

        matcher = etree.HTML(resp.text)
        url = matcher.xpath("//img/../@href")
        del matcher

        if url == []:
            continue

        pics.append({
            "url": url[0],
            "date": tmp
        })
    
    for pic in pics[::-1]:
        if not chk_line("apod", pic["date"], _db):
            add_line("apod", pic["date"], pic["url"], _db)

if __name__ == "__main__":
    database = sqlite3.connect('./picture.db')
    update_bing(database)
    update_apod(database)

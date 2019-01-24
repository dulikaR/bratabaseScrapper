import requests
import pymysql


def download_pic( url, i):
    name = str(i)
    url = str(url)
    result = requests.get(url, stream=True)
    if result.status_code == 200:
        image = result.raw.read()
        open(name, "wb").write(image)


def download_db():
    db = pymysql.connect("localhost", "root", "", "bratabase")
    cursor = db.cursor()
    cursor.execute("SELECT url FROM image")
    result_set = cursor.fetchall()
    print("done")
    i=0
    for url in result_set:
        i+=1
        download_pic( url[0], i)


download_db()
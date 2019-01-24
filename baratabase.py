import requests
from bs4 import BeautifulSoup
import pymysql



def get_page_links(db,urlName):
    soup = BeautifulSoup(requests.get(urlName).content)

    item_link = soup.find_all('a', attrs={'class': 'fit-request-list-item'})
    for single_item_link in item_link:
        item_href = single_item_link['href']
        page_link = "https://www.bratabase.com" + str(item_href)
        print(page_link)

        STMT = 'INSERT INTO itemlinks (link) VALUES (%s)'
        rows = [( str(page_link))]
        db.cursor().executemany(STMT, rows)
        db.commit()

def start():
    db = pymysql.connect("localhost", "root", "", "bratabase")

    for x in range(183):
      print(x+1)
      numOne = str(x+1)
      url = str('https://www.bratabase.com/troubleshoot/closed/?page='+numOne)
      get_page_links(db,url)


    for x in range(20):
      print(x+1)
      numTwo = str(x + 1)
      url = str('https://www.bratabase.com/troubleshoot/?page=' + numTwo)
      get_page_links(db,url)


start()
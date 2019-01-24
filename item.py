import requests
from bs4 import BeautifulSoup
import pymysql



def intergrate(db,urlName,num):

    soup = BeautifulSoup(requests.get(urlName).content)
    item_id = num
    #header
    # header = soup.find( 'h1', attrs={'id': 'content-header'} ).text
    # print(header)

    #image
    image_links = soup.find_all( 'a', attrs={'class': 'pic-box'} )
    for image_items in image_links:
        image = image_items.find( 'img' )
        src =  str(image['src'])
        alt =  str(image['alt'])
        STMT = 'INSERT INTO image (itemId,url,alt) VALUES (%s,%s,%s)'
        rows = [(item_id,src,alt)]
        db.cursor().executemany(STMT, rows)
        db.commit()

    #user Review
    user_review = soup.find( 'div', attrs={'class': 'user-review'} ).text
    k = user_review.split("\n\n")

    issueResolved = str(k[1])
    originalProblem = str(k[3])
    STMT = 'INSERT INTO userreview (itemId,issueResolved,originalProblem) VALUES (%s,%s,%s)'
    rows = [(item_id, issueResolved, originalProblem)]
    db.cursor().executemany(STMT, rows)
    db.commit()

    fit_issues = k[6].split("\n")
    problemType = fit_issues[0:][::2]  # even
    problem = fit_issues[1:][::2]  # odd
    number  = len(problemType)
    for i in range(number):
        pt = str(problemType[i])
        try:
            p = str(problem[i])
        except:
            p = 'null'

        STMT = 'INSERT INTO fitissues (itemId,problemType,problem) VALUES (%s,%s,%s)'
        rows = [(item_id, pt, p)]
        db.cursor().executemany(STMT, rows)
        db.commit()


    #suggestions2
    suggestions = soup.find_all( 'li', attrs={'class': 'highlight-on-target'} )
    for suggestion in suggestions:

        try:
            suggestion_main = suggestion.find( 'div', attrs={'class': 'grid_9'} ).text
            suggestion_db = suggestion_main
            suggestionComment_db = 'null'
        except:
            suggestion_db = 'null'
            suggestionComment_db = str(suggestion.text)

        STMT = 'INSERT INTO suggestions (itemId,suggestion,suggestionComment) VALUES (%s,%s,%s)'
        rows = [(item_id, suggestion_db, suggestionComment_db)]
        db.cursor().executemany(STMT, rows)
        db.commit()

    print("finish")



def get_page_links(db,urlName,num):
    soup = BeautifulSoup(requests.get(urlName).content)
    number = 0.00
    item_link = soup.find_all('a', attrs={'class': 'fit-request-list-item'})
    for single_item_link in item_link:
        number += 0.01
        total_num = int(num)+number
        item_href = single_item_link['href']
        page_link = "https://www.bratabase.com" + str(item_href)
        print(page_link)
        intergrate(db,page_link,total_num)

def start():
    db = pymysql.connect("localhost", "root", "", "bratabase")

    for x in range(183):
      print(x+1)
      numOne = str(x+1)
      url = str('https://www.bratabase.com/troubleshoot/closed/?page='+numOne)
      get_page_links(db,url,numOne)


    for x in range(20):
      print(x+1)
      numTwo = str(x + 1)
      url = str('https://www.bratabase.com/troubleshoot/?page=' + numTwo)
      get_page_links(db,url,numTwo)

start()
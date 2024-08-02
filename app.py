from bs4 import BeautifulSoup
import html
import requests
from fastapi import FastAPI
import uvicorn

app = FastAPI()

url = "https://sites.google.com/view/ggsipuedc/notice-board?authuser=0"
webpage = requests.get(url=url)
soup = BeautifulSoup(webpage.content, 'lxml')

def getNotices(soup):
    divs = soup.find_all('div', {'class': 'w536ob'})
    data = []

    for div in divs:
        data_code_content = div.get('data-code')
        decoded_content = html.unescape(data_code_content)
        soup_decoded = BeautifulSoup(decoded_content, 'lxml')
        rows = soup_decoded.find_all('tr')
        for row in rows[1:]:
            columns = row.find_all('td')
            if len(columns) >= 2:
                date = columns[0].text.strip()
                link = columns[1].find('a')
                if link is not None:
                    title = link.text.strip()
                    href = link.get('href')
                    data.append({'date': date, 'title': title, 'link': href})
    return data

@app.get("/get")
async def get_Notices():
    return getNotices(soup)

from bs4 import *
from web_connector import web_connector


def parse(web_address):
    films = {}

    connector = web_connector()
    page = connector.open_page(web_address)
    if page != None:
        soup_page = BeautifulSoup(page.read())
        try:
            divs_a = soup_page.findAll("div", {"class": "row_a clearfix"})
            for item in divs_a:
                name = item.findAll("div", {"class": "author"})[0].findAll("a")[0].text
                rating = item.findAll("div", {"class": "rating"})[0].findAll("h4")[0].text
                films[name] = int(rating)
            divs_b = soup_page.findAll("div", {"class": "row_b clearfix"})
            for item in divs_b:
                name = item.findAll("div", {"class": "author"})[0].findAll("a")[0].text
                rating = item.findAll("div", {"class": "rating"})[0].findAll("h4")[0].text
                films[name] = int(rating)
        except:
            pass
    return films


if __name__ == "__main__":
    print(parse('http://www.kritikanstvo.ru/critics/1795/'))
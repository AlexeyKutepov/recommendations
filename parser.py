from bs4 import *
from web_connector import web_connector

import re


def parse_critic(web_address):
    """
    Парсер страницы критиков
    :param web_address: адрес страницы критика
    :return: оценки критика к фильмам
    """
    films = {}
    connector = web_connector()
    page = connector.open_page(web_address)
    if page != None:
        soup_page = BeautifulSoup(page.read())
        try:
            divs_a = soup_page.findAll("div", {"class": "row_a clearfix"})
            for item in divs_a:
                name = item.findAll("div", {"class": "author"})[0].findAll("a")[0].text
                rus_letters = re.findall('[А-Яа-я]', name)
                lat_letters = re.findall('[A-Za-z]', name)
                if len(rus_letters) == 0 and len(lat_letters) > 0:
                    continue
                rating = item.findAll("div", {"class": "rating"})[0].findAll("h4")[0].text
                films[name.strip()] = int(rating)
            divs_b = soup_page.findAll("div", {"class": "row_b clearfix"})
            for item in divs_b:
                name = item.findAll("div", {"class": "author"})[0].findAll("a")[0].text
                rus_letters = re.findall('[А-Яа-я]', name)
                lat_letters = re.findall('[A-Za-z]', name)
                if len(rus_letters) == 0 and len(lat_letters) > 0:
                    continue
                rating = item.findAll("div", {"class": "rating"})[0].findAll("h4")[0].text
                films[name.strip()] = int(rating)
        except:
            pass
    return films


def parse_film(web_address):
    """
    Парсер страниц фильмов
    :param web_address: адрес страницы фильма
    :return: оценки критиков фильма
    """
    result = {}
    connector = web_connector()
    page = connector.open_page(web_address)
    if page != None:
        soup_page = BeautifulSoup(page.read())
        try:
            film_name = soup_page.findAll("span", {"itemprop": "name"})[0].text
            divs_a = soup_page.findAll("div", {"class": "row_a clearfix"})
            for item in divs_a:
                name = item.findAll("div", {"class": "author"})[0].findAll("a")[0].text
                rating = item.findAll("div", {"class": "rating"})[0].findAll("h4")[0].text
                result[name.strip()] = {film_name: int(rating)}
                link = 'http://www.kritikanstvo.ru' + item.findAll("div", {"class": "author"})[0].findAll("a")[0]['href']
                critic = parse_critic(link)
                result[name.strip()].update(critic)
            divs_b = soup_page.findAll("div", {"class": "row_b clearfix"})
            for item in divs_b:
                name = item.findAll("div", {"class": "author"})[0].findAll("a")[0].text
                rating = item.findAll("div", {"class": "rating"})[0].findAll("h4")[0].text
                result[name.strip()] = {film_name: int(rating)}
                link = 'http://www.kritikanstvo.ru' + item.findAll("div", {"class": "author"})[0].findAll("a")[0]['href']
                critic = parse_critic(link)
                result[name.strip()].update(critic)
        except:
            pass
    return result


if __name__ == "__main__":
    # Список фильмов
    films = [
        'http://www.kritikanstvo.ru/movies/spidermanhomecoming/',
        'http://www.kritikanstvo.ru/movies/tesnota/',
        'http://www.kritikanstvo.ru/movies/windriver/',
        'http://www.kritikanstvo.ru/movies/waroftheplanetoftheapes/',
        'http://www.kritikanstvo.ru/movies/dunkirk/',
        'http://www.kritikanstvo.ru/movies/atomicblonde/',
        'http://www.kritikanstvo.ru/movies/cars3/',
        'http://www.kritikanstvo.ru/movies/blokbaster/',
        'http://www.kritikanstvo.ru/movies/darktower/',
        'http://www.kritikanstvo.ru/movies/security/',
        'http://www.kritikanstvo.ru/movies/ladymacbeth/',
        'http://www.kritikanstvo.ru/movies/kidnap/',
        'http://www.kritikanstvo.ru/movies/sonofbigfoot/',
        'http://www.kritikanstvo.ru/movies/thebeguiled/',
        'http://www.kritikanstvo.ru/movies/johnwickchaptertwo/',
        'http://www.kritikanstvo.ru/movies/djangounchained/',
        'http://www.kritikanstvo.ru/movies/lalaland/',
        'http://www.kritikanstvo.ru/movies/godfather/',
        'http://www.kritikanstvo.ru/movies/thebigshort/',
        'http://www.kritikanstvo.ru/movies/interstellar/',
        'http://www.kritikanstvo.ru/movies/startrekintodarkness/',
        'http://www.kritikanstvo.ru/movies/startrekbeyond/'
    ]

    rus_critics = {}

    for film in films:
        print(film)
        result = parse_film(film)
        for key in result:
            if key in rus_critics.keys():
                rus_critics[key].update(result[key])
            else:
                rus_critics[key] = result[key]
    print(rus_critics)

"""
Модуль отвечающий за установку соединения c интернет-ресурсом
"""

__author__ = 'Alexey Kutepov'


import urllib.request
import urllib.error

# Данный класс содержит методы, отвечающие за установку соединения с необходимым интернет-ресурсом
# При необходимости есть возможность авторизации для работы через прокси-сервер
class web_connector:

    def __init__(self, login=None, password=None):
        self.login = login
        self.password = password

    # Метод для установки соединения с ресурсом через прокси-сервер
    # Возвращает открытую страницу
    def open_with_authentication(self, web_address):
        address_port = urllib.request.getproxies()['http']
        address_port = address_port.split("http://")[1]
        proxy = urllib.request.ProxyHandler({'http': r'http://'+self.login+':'+self.password+'@'+address_port})
        authentication = urllib.request.HTTPBasicAuthHandler()
        opener = urllib.request.build_opener(proxy, authentication, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
        page = urllib.request.urlopen(web_address)
        return page

    # Метод возвращает открытую страницу, при неудаче вызывает метод open_with_authentication
    def open_page(self, web_address):
        try:
            page = urllib.request.urlopen(web_address)
        except urllib.error.HTTPError as e:
            if e.code==407:
                try:
                    page = self.open_with_authentication(web_address)
                except:
                    raise IOError("Error:",e,"; can't open page", web_address)
            else:
                raise IOError("Error:",e,"; can't open page", web_address)
        return page

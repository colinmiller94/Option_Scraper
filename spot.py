from bs4 import BeautifulSoup
import urllib.request


#returns spot as float
def get_spot(url):
    """
    :param url: real-time price url, must be from nasdaq's site
    :return: spot price
    """

    source = urllib.request.urlopen(url)
    content = source.read().decode('utf-8')

    soup = BeautifulSoup(content, 'html.parser')
    price = soup.find('div', {'id': 'qwidget_lastsale'}).text

    price = float(price[1:])
    return price





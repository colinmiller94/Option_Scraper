from bs4 import BeautifulSoup
import urllib.request


#returns spot as float
def get_spot(url):

    source = urllib.request.urlopen(url)
    content = source.read().decode('utf-8')

    soup = BeautifulSoup(content, 'html.parser')
    price = soup.find('div', {'id': 'qwidget_lastsale'}).text

    price = float(price[1:])
    return price





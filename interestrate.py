from bs4 import BeautifulSoup
import urllib.request
def interest_rate(t):
    #input time to expiration, in years
    #return applicable spot rate based on LIBOR rates

    ends = ['overnight.aspx', '1-week.aspx', '1-month.aspx', '2-months.aspx', '3-months.aspx', '6-months.aspx', '12-months.aspx']
    url = 'http://www.global-rates.com/interest-rates/libor/american-dollar/usd-libor-interest-rate-'
    url_list =[url + end for end in ends]


    rates =[]
    for url in url_list:
        source = urllib.request.urlopen(url)
        content = source.read().decode('utf-8')

        soup = BeautifulSoup(content, 'html.parser')
        bigstring = soup.find('tr', {'class': 'tabledata1'}).text

        i = 0
        while i < len(bigstring):
            if bigstring[i] == '.':
                dot_index = i

            i+= 1
        rate = bigstring[dot_index-1: dot_index+5]

        rates.append(rate)


    t = t * 365.0

    rates = [float(i) for i in rates]

    if t <= 1:
        return rates[0]
    elif t <= 7:
        return rates[0] +(rates[1] - rates[0]) * (t -1)/6
    elif t <= 30:
        return rates[1] +(rates[2] - rates[1]) * (t -7)/23
    elif t <= 60:
        return rates[2] +(rates[3] - rates[2]) * (t-30)/30
    elif t <= 90:
        return rates[3] +(rates[4] - rates[3]) * (t-60)/30
    elif t <= 180:
        return rates[4] +(rates[5] - rates[4]) * (t-90)/90
    elif t <= 360:
        return rates[5] +(rates[6] - rates[5]) * (t-180)/180

    else:
        print('that expires too far away what you doin')
    #print(tables)




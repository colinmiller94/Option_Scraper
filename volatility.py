import pandas as pd
import math
import urllib.request
from bs4 import BeautifulSoup
import datetime
import matplotlib.pylab as plt
from pricer import Theo, Vega


sec = 'SPY'



monthdict = {'Jan': '01', 'Feb': '02', 'Mar': '03',
             'Apr': '04', 'May': '05', 'Jun': '06',
             'Jul': '07', 'Aug': '08', 'Sep': '09',
             'Oct': '10', 'Nov': '11', 'Dec': '12'}


#From this format (Apr 05, 3017) to datetime.date object
def convert_date(dstring):
    newstring = dstring[8:] + '-' +monthdict[dstring[0:3]] + '-' + dstring[4:6]
    newstring = datetime.datetime.strptime(newstring, '%Y-%m-%d').date()
    return newstring


def get_vol (url, num_days):
    source = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(source,'lxml')

    tables = soup.find('table')
    table_rows = tables.find_all('tr')

    closes = []

    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        #print(row)

        if len(row) == 7:
            closes.append(float(row[4]))

    i = 0
    returns = []


    while i < num_days:

        daily_return = math.log(closes[i] /closes[i+1])
        returns.append(daily_return)
        i +=1

    #square returns, sum, square root
    ret_sq = [i ** 2 for i in returns]
    sumsq = sum(ret_sq)
    rss =  math.sqrt(sumsq)
    scalar = math.sqrt(252/num_days)
    ann_vol = scalar * rss

    return ann_vol


# list of num_days to consider
def get_vol_hist (security, num_days, days_back):

    url = 'https://finance.yahoo.com/quote/' + security + '/history?p=' + security
    source = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(source,'lxml')

    tables = soup.find('table')
    table_rows = tables.find_all('tr')

    dates = []
    closes = []

    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        #print(row)

        if len(row) == 7:
            closes.append(float(row[4]))
            dates.append(row[0])


    i = 0
    returns = []


    while i < max(num_days) + days_back:

        daily_return = math.log(closes[i] /closes[i+1])
        returns.append(daily_return)
        i +=1

    i = 0
    ann_vols = []
    while i < days_back:
        ann_vol = []
        for j in num_days:
            temp_returns = returns[i:j + i]
            ret_sq = [i ** 2 for i in temp_returns]
            sumsq = sum(ret_sq)
            rss = math.sqrt(sumsq)
            scalar = math.sqrt(252 / j)
            ann_vol.append(scalar * rss)
        ann_vols.append(ann_vol)
        i+= 1


    #Read old dataframe from excel
    try:
        xl = pd.ExcelFile(security + "RealVol.xlsx")
        old_df = xl.parse('RealizedVol')
        #print(old_df)

        num_days = [str(i) + ' day vol' for i in num_days]

        df = pd.DataFrame(columns = num_days,  data = ann_vols, index = dates[0:days_back])

        combined_df = pd.concat([df,old_df])


    except FileNotFoundError:
        num_days = [str(i) + ' day vol' for i in num_days]
        df = pd.DataFrame(columns=num_days, data=ann_vols, index=dates[0:days_back])
        combined_df = df

    #remove duplicates
    new_df = pd.DataFrame(columns =num_days, data  = [])
    for index, row in combined_df.iterrows():
        if index not in new_df.index:
            new_df = new_df.append(row)


    writer = pd.ExcelWriter(security+'RealVol.xlsx')
    new_df.to_excel(writer, 'RealizedVol')

    writer.save()

    return new_df


#Gets out of the money options at strike and +/-
def plotImpVol(call, put, spot, security):
    x = []
    y = []
    call_iv = call.ix[call['Strike'] > spot].ix[call['Strike'] < spot + 10.0]
    put_iv = put.ix[put['Strike'] < spot].ix[put['Strike'] > spot - 10.0]



    for index, row in put_iv.iterrows():
        x.append(row['Strike'])
        y.append(float(row['Calc Imp Vol'][0:5]))

    for index, row in call_iv.iterrows():
        x.append(row['Strike'])
        y.append(float(row['Calc Imp Vol'][0:5]))

    fig,axis = plt.subplots()
    plt.plot(x,y, marker = '.', linestyle = 'solid')
    plt.title(security + 'ImpliedVol' + ' Spot: ' + str(spot))
    fig.savefig(security + 'ImpliedVol.png')
    plt.close('all')

def plotVolSeries(security):
    #input string
    df = get_vol_hist(security, [10,20,30,50], 40)
    dates = []
    for day in df.index:
        date = convert_date(day)
        dates.append(date)
    headers = list(df)
    fig, axis = plt.subplots()

    i = 0
    while i < len(headers):
        plt.plot(dates, df[headers[i]], marker = '.',  linestyle ='solid', label = headers[i])
        i += 1

    plt.legend(loc = 'best')
    fig.autofmt_xdate()
    plt.title(security + 'Realized Vol')
    fig.savefig(security+'RealizedVol.png')
    plt.close('all')


#plotVolSeries('SPY')


#attempt at backing out vol, behaves too weird sometimes

def ImpliedVol(Type, S, X, t, r, b, price, volguess):

    i = 0

    while i < 100:
        priceguess = Theo(Type,S,X,t,r,b,volguess)
        vega = Vega(S, X, t, r, b, volguess)
        diff = price - priceguess
        if abs(diff) < .001:
            return volguess

        volguess = volguess + diff/(vega *100)
        i+=1
    return volguess


#print(Theo('C', 115, 120, .13, .02, 0,.26))

#print(ImpliedVol('C', 115,120, .13, .02, 0, 2.33132, .49))

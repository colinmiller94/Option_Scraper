import pandas as pd
from pricer import Theo, Delta, Gamma, Theta, Vega
from spot import get_spot
from volatility import get_vol, plotImpVol, plotVolSeries, ImpliedVol
import statistics
from timestamp import get_tte
from interestrate import interest_rate
from twilio.rest import Client



expiration = '2018-07-06'
sec = 'SPY'

url = 'https://finance.yahoo.com/quote/'+ sec + '/options?p=' + sec
#spot_url = 'https://finance.yahoo.com/quote/SPY?p=SPY'
spot_url = 'https://www.nasdaq.com/symbol/'+ sec + '/real-time'
vol_url = 'https://finance.yahoo.com/quote/'+ sec + '/history?p=' + sec

def main():
    """
    Creates dataframe given security and expiration, runs options through pricer,
    generates risk characteristic excel sheet, creates vol graphs
    :return:
    """
    tte, url_pt2 =  get_tte(expiration)
    url2 = url + '&date=' + url_pt2
    dfs = pd.read_html(url2)

    call_df = dfs[0]
    put_df = dfs[1]
    
    
    """Should have created an Option class here. Like:
    class Option:
        def __init__(self,type, spot, strike, time, rate, div, vol, vol_guess,price):
            self.type = type
            self.spot = spot
            .....
        def theo(self):
            return Theo(type, spot, strike,time, rate, div, vol)
        def delta(self):
            return Delta(type, spot, strike,time, rate, div, vol)
        ...
   
    """
    
    
    #instead, a bunch of lists: 
    call_theos = []
    put_theos = []
    call_vols= []
    put_vols= []

    call_deltas = []
    call_gammas = []
    call_thetas = []
    call_vegas = []
    put_deltas = []
    put_gammas = []
    put_thetas = []
    put_vegas = []

    call_imp_vols =[]
    put_imp_vols = []

    spot = get_spot(spot_url)
    print('Spot:', spot)
    vol = get_vol(vol_url,20)
    print('20day Vol:' ,vol)
    rate = interest_rate(tte)
    div = .0

    #Don't really care about options going for pennies
    call_df = call_df.ix[call_df['Volume'] >=100].ix[call_df['Last Price'] >= .10]
    put_df = put_df.ix[put_df['Volume'] >= 100].ix[put_df['Last Price'] >= .10]


    for index, row in call_df.iterrows():
        call_vol = row['Implied Volatility'][:-1]
        call_vols.append(float(call_vol))


    for index, row in put_df.iterrows():
        put_vol = row['Implied Volatility'][:-1]
        put_vols.append(float(put_vol))


    # extremely crude method for increasing put vol to help account for skew
    call_sd = statistics.stdev(call_vols)
    call_mean = sum(call_vols)/len(call_vols)
    call_vols = [vol for vol in call_vols if abs(vol-call_mean) <= 3 * call_sd]
    call_vol_factor = sum(call_vols)/len(call_vols) / 100.0

    put_sd = statistics.stdev(put_vols)
    put_mean = sum(put_vols)/len(put_vols)
    put_vols = [vol for vol in put_vols if abs(vol-put_mean) <= 1 * put_sd]
    put_vol_factor = sum(put_vols)/len(put_vols) / 100.0

    call_vol = vol
    put_vol = vol * (put_vol_factor/call_vol_factor)

    for index, row in call_df.iterrows():
        strike = float(row['Strike'])
        time = tte
        call_theos.append(Theo('C', spot, strike, time, rate, div, call_vol))
        call_deltas.append(Delta('C', spot, strike, time, rate, div, call_vol))
        call_gammas.append(Gamma(spot, strike, time, rate, div, call_vol))
        call_thetas.append(Theta('C', spot, strike, time, rate, div, call_vol))
        call_vegas.append(Vega(spot, strike, time, rate, div, call_vol))


        midpoint = (float(row['Bid']) + float(row['Ask']))/2.0
        call_imp_vols.append(ImpliedVol('C', spot,strike,time,rate,div,midpoint, call_vol))

    for index, row in put_df.iterrows():
        strike = float(row['Strike'])
        time = tte
        put_theos.append(Theo('P', spot, strike, time, rate, div, put_vol))
        put_deltas.append(Delta('P', spot, strike, time, rate, div, put_vol))
        put_gammas.append(Gamma(spot, strike, time, rate, div, put_vol))
        put_thetas.append(Theta('P', spot, strike, time, rate, div, put_vol))
        put_vegas.append(Vega(spot, strike, time, rate, div, put_vol))

        midpoint = (float(row['Bid']) + float(row['Ask'])) / 2.0
        put_imp_vols.append(ImpliedVol('P', spot, strike, time, rate, div, midpoint, put_vol))


    call_df['Theo'] = call_theos
    call_df['Delta'] = call_deltas
    call_df['Gamma'] = call_gammas
    call_df['Theta'] = call_thetas
    call_df['Vega'] = call_vegas

    put_df['Theo'] = put_theos
    put_df['Delta'] = put_deltas
    put_df['Gamma'] = put_gammas
    put_df['Theta'] = put_thetas
    put_df['Vega'] = put_vegas

    call_imp_vols = [str(i*100)[0:5] + '%' for i in call_imp_vols]
    put_imp_vols = [str(i*100)[0:5] + '%' for i in put_imp_vols]

    call_df['Calc Imp Vol'] =call_imp_vols
    put_df['Calc Imp Vol'] = put_imp_vols


    #Message alert for large discrepancies between theo and midpoint of bid/ask
    default = sec+ ' Alert ' + expiration + '\n'
    alertstring = default
    for index, row in call_df.iterrows():

        midpoint = (float(row['Ask']) + float(row['Bid']))/2.0
        if abs(row['Theo'] - midpoint  ) >= 1.0:

            edge = str(abs(row['Theo'] - midpoint))
            if row['Theo'] > midpoint:
                updown = 'under'
            else:
                updown = 'over'


            alertstring += str(int(row['Strike'])) + 'C ' + edge[0:4] + ' ' + updown + '\n'

    for index, row in put_df.iterrows():

        midpoint = (float(row['Ask']) + float(row['Bid'])) / 2.0
        if abs(row['Theo'] - midpoint) >= 1.0:

            edge = str(abs(row['Theo'] - midpoint))
            if row['Theo'] > midpoint:
                updown = 'under'
            else:
                updown = 'over'

            alertstring += str(int(row['Strike'])) + 'P ' + edge[0:4] + ' ' + updown +  '\n'
    if alertstring != default:
        send_message(alertstring)

    plotVolSeries(sec)
    plotImpVol(call_df,put_df,spot, sec)
    writer = pd.ExcelWriter(sec+'_options_' + expiration +'.xlsx')
    call_df.to_excel(writer, 'Calls')
    put_df.to_excel(writer, 'Puts')
    writer.save()



def send_message(string):
    """
    :param string: Alert message string
    :return:
    """
    account_sid = 'asdf'
    auth_token = 'asdf'

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to = 'asdf',
        from_ = 'asdf ',
        body = string)

main()

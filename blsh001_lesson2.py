#same code as the one used for Lesson 1 in blsh001_lesson1.py, but having the "flattish" variable changed to 0.8
import pandas as pd
import requests



#the function to get the individual stock pricing data
def get_data_api(stock):
    """
    function calls the IEX API and returns a pandas df of it. Make sure it starts with oldest date
    """
    data=requests.get('https://cloud.iexapis.com/stable/stock/{}/chart/max?token={YOUR_TOKEN_HERE}'.format(stock.lower()))
    try:
        dataj=data.json()
    except:
        return 'Error in get_data_api for {}.'.format(stock)
    data_list=list()
    for i in dataj:
        data_list.append([i['date'], i['open'], i['close'], i['low'], i['high'], i['volume']])
    df=pd.DataFrame(data_list, columns=['date', 'open', 'close', 'low', 'high', 'volume'])
    return df


def trading_flattish(data, sell_off_v, time_l, wait_t, loss_cut_v, position_sell):
    #getting the daily "close" prices percentage changes, and putting them in a new column 'changes'
    data['change']=data['close'].pct_change()
    data=data.fillna(0) #replacing all NaN values with 0
    #defining the size of the flattish variable
    flattish=data['change'].std()
    #initiating the list that holds our trades
    positions=list()
    #initiating our indexing variable
    pos=0
    while pos<len(data)-time_l-wait_t-1:
        if data['change'].iloc[pos]<-sell_off_v:
            #checking if prices are flattish over the next 10 days
            if data['change'][pos:pos+time_l].std()<0.8*flattish:
                #finding the next value where overall performance > position_sell
                for kk in range(wait_t):
                    perf=data['close'].iloc[pos+time_l+kk]/data['close'].iloc[pos+time_l]
                    if perf>position_sell:
                        break
                    if perf<loss_cut_v:
                        break
                #check if a loss_cut even occurs during the [starting, ending] period
                positions.append([data['date'].iloc[pos+time_l], data['date'].iloc[pos+kk+time_l],perf,pos+time_l,pos+kk+time_l])
                pos=pos+kk+time_l
            else:
                pos=pos+1
        else:
            pos=pos+1 #we are increasing the starting position by 1
    return positions

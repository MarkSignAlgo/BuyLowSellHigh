#the BuyLowSellHigh algorithm with a dynamic loss-cut function that can execute throughout the day
def trading_flattish_dlc(data, sell_off_v, time_l, wait_t, loss_cut_v, position_sell):
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
                    lc_perf=data['close'].iloc[pos+time_l+kk]/data['close'].iloc[pos+time_l]
                    if lc_perf<loss_cut_v:
                        positions.append([data['date'].iloc[pos+time_l], data['date'].iloc[pos+kk+time_l],lc_perf,pos+time_l,pos+kk+time_l])
                        break
                    if perf>position_sell:
                        positions.append([data['date'].iloc[pos+time_l], data['date'].iloc[pos+kk+time_l],perf,pos+time_l,pos+kk+time_l])
                        break
                pos=pos+kk+time_l
            else:
                pos=pos+1
        else:
            pos=pos+1 #we are increasing the starting position by 1
    return positions
  
  #backtesting function that identifies the best variables to maximize returns
  

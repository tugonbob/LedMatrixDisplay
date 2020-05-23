import requests

#stock tickers in 2020 Dow Jones Industrial Average
dow = ['MMM', 'AXP', 'AAPL', 'BA', 'CAT', 'CVX', 'CSCO', 'KO', 'DOW', 'XOM', 'GS', 'HD', 'IBM', 'INTC', 'JNJ', 'JPM', 'MCD', 'MRK', 'MSFT', 'NKE', 'PFE', 'PG', 'RTX', 'TRV', 'UNH', 'VZ', 'V', 'WMT', 'WBA', 'DIS']
#my personal watchlist
watchlist = ['BABA', 'DIS', 'AAPL', 'SHOP', 'SNE']
demolist = ['BABA', 'AAPL', 'TSLA', 'SPOT']

#return the Ticker, CurrentPrice, and the PercentChange
#example return string: "`rMMM 145.81<2.59   `rAAPL 316.85<0.75   `gTSLA 830.8>1.87   "
#the '`g' symbolize color change, and the '<' displays down arrow, and the '>' displays up arrows
def get_stock_info():
    string = ""
    for ticker in demolist:
        r = requests.get('https://finnhub.io/api/v1/quote?symbol={}&token=br3gbbnrh5rai6tghkig'.format(ticker))
        data = r.json()
        
        current_price = round( data['c'], 2) # round current price to 2 decimal places
        previous_close = data['pc']
        percent_change = round( ( current_price - previous_close ) / previous_close * 100, 2) #percent change from previous day close to current price, rounded to 2 decimal points
        
        if (percent_change < 0): #if stock price goes down
            string = string + "`r`" + ticker + " " + str(current_price) + "<" + str(abs(percent_change)) + "   "
        elif (percent_change > 0): #if stock price goes up
            string = string + "`g`" + ticker + " " + str(current_price) + ">" + str(abs(percent_change)) + "   "
        else: #if stock price hasn't changed 
            string = string + "`y`" + ticker + " " + str(current_price) + "-" + "0.00" + "   "
    return string

#return 2 most recent headlines on each company
#example return str: `gBABA: `yBears book nearly $400 million from legislation aimed at stopping China from ‘cheating’’,  SoftBank Group to Sell $3 Billion Stake in Japanese Wireless Company   `gDIS: `yUniversal Orlando eyes early June for reopening theme parks,  Dow drops nearly 150 points on losses for Walt Disney, Coca-Cola stocks   `gAAPL: `yRaise Your Bets On Xiaomi (OTCMKTS:XIACF),  Tech giants are embracing remote work. Others may follow   `gSHOP: `yDow ends week 455 points higher, shaking off the worst U.S. unemployment rate since the Great Depression,  Will Shopify (SHOP) Be The Next Amazon?   `gSNE: `yAlhambra Investment Partners LLC Cuts Position in Sony Corp (NYSE:SNE),  Envestnet Asset Management Inc. Grows Position in Sony Corp (NYSE:SNE)
def get_stock_news():
    string = ""
    for ticker in watchlist:
        r = requests.get('https://finnhub.io/api/v1/company-news?symbol={}&from={}&to={}&token=br3gbbnrh5rai6tghkig'.format(ticker, '2020-04-22', '2020-05-22'))
        data = r.json()
        string = string + "`g`" + ticker + ": `y`" + str(data[0]['headline']) + ",  " + str(data[1]['headline']) + "   "
    return string

        
        
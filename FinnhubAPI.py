import requests

#stock tickers in 2020 Dow Jones Industrial Average
dow = ['MMM', 'AXP', 'AAPL', 'BA', 'CAT', 'CVX', 'CSCO', 'KO', 'DOW', 'XOM', 'GS', 'HD', 'IBM', 'INTC', 'JNJ', 'JPM', 'MCD', 'MRK', 'MSFT', 'NKE', 'PFE', 'PG', 'RTX', 'TRV', 'UNH', 'VZ', 'V', 'WMT', 'WBA', 'DIS']

def get_stock_info():
    string = ""
    for ticker in dow:
        r = requests.get('https://finnhub.io/api/v1/quote?symbol={}&token=br3gbbnrh5rai6tghkig'.format(ticker))
        data = r.json()
        
        current_price = data['c']
        previous_close = data['pc']
        percent_change = round( ( current_price - previous_close ) / previous_close * 100, 2) #percent change from previous day close to current price, rounded to 2 decimal points
        
        if (percent_change < 0): #if stock price goes down
            string = string + "   `r" + ticker + " " + str(current_price) + "<" + str(abs(percent_change))
        elif (percent_change > 0): #if stock price goes up
            string = string + "   `g" + ticker + " " + str(current_price) + ">" + str(abs(percent_change))
        else: #if stock price hasn't changed
            string = string + "   `y" + ticker + " " + str(current_price) + "-" + "0.00"
    return string
        
#example return string: "   `rMMM 145.81<2.59   `rAAPL 316.85<0.75   `gTSLA 830.8>1.87"
#the '`g' symbolize color change, and the '<' displays down arrow, and the '>' displays up arrows
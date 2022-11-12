import pandas_datareader.data as web
import datetime as dt
import pandas as pd
from functools import reduce 

class Dataloader():
	def __init__(self, start, end, stocks):
		self.start = start
		self.end = end
		self.stocks = stocks
		self.tickers = list(stocks.keys())
		self.df = None

	def _get(self, ticker):
		d = web.DataReader(ticker, "yahoo", self.start, self.end)
		d[ticker] = d['Close']
		return d[[ticker]]

	def get(self):
		df = [self._get(x) for x in self.stocks]
		self.df = reduce(lambda l, r: pd.merge(l, r, on=['Date'], how='outer'), df)
		return self.df

	def calc_return(self):
		df = self.get() if not self.df else self.df
		for t in self.tickers:
			p, q = self.stocks[t]
			df[t] = df[t].map(lambda x : (x-p)/p)
		return df

if __name__ == '__main__':
	data = Dataloader(dt.datetime(2022, 9, 1), dt.datetime.today(), ["META", "AAPL"])
	df = data.get()
	print(df)

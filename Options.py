import robin_stocks as r
import sqlite3
import datetime
from time import sleep
from os.path import expanduser
import logging
import random

def getData(stock):
	print(stock)
	tradable = r.options.find_tradable_options_for_stock(stock)
	price = r.stocks.get_latest_price(stock)[0]
	dates = set()
	for option in tradable:
		dates.add(option['expiration_date'])
	home = expanduser('~')
	directory = home+'/trading/data/'
	conn = sqlite3.connect(directory+stock+'.db')
	c = conn.cursor()
	logging.basicConfig(filename=home+'/trading/error', level=logging.WARNING)
	for date in dates:
		try:
			c.execute('''SELECT count(name) FROM sqlite_master WHERE
				type="table" AND name="{0}" '''.format(date))
			if c.fetchone()[0] == 0:
				c.execute('''CREATE TABLE "{0}" (
					strike_price REAL,
					update_time TEXT,
					type TEXT,
					underlying_price REAL,
					bid_price REAL,
					ask_price REAL,
					bid_size INTEGER,
					ask_size INTEGER,
					low_price REAL,
					high_price REAL,
					mark_price REAL,
					open_interest INTEGER,
					volume INTEGER,
					chance_of_profit_long REAL,
					chance_of_profit_short REAL,
					delta REAL,
					gamma REAL,
					rho REAL,
					theta REAL,
					vega REAL,
					implied_volatility REAL,
					high_fill_rate_buy_price REAL,
					high_fill_rate_sell_price REAL,
					low_fill_rate_buy_price REAL,
					low_fill_rate_sell_price REAL
				) '''.format(date))
				c.execute('CREATE INDEX "idx_{0}" ON "{1}" (strike_price, update_time)'.format(date, date))
		except Exception as e:
			message = "Failed to create table {0}, {1} ---- {2}".format(date, stock, datetime.datetime.utcnow())
			print(message)
			logging.warning(message+'\n'+str(e))
		try:
			data = r.options.find_options_for_stock_by_expiration(stock, date)
		except Exception as e:
			message = "Failed to retrieve option data {0}, {1} ---- {2}".format(date, stock, datetime.datetime.utcnow())
			print(message)
			logging.warning(message+'\n'+str(e))
			continue
		for d in data:
			string = '''INSERT INTO "{0}" (
					strike_price,
					update_time,
					type,
					underlying_price,
					bid_price,
					ask_price,
					bid_size,
					ask_size,
					low_price,
					high_price,
					mark_price,
					open_interest,
					volume,
					chance_of_profit_long,
					chance_of_profit_short,
					delta,
					gamma,
					rho,
					theta,
					vega,
					implied_volatility,
					high_fill_rate_buy_price,
					high_fill_rate_sell_price,
					low_fill_rate_buy_price,
					low_fill_rate_sell_price
				) VALUES (
					{1},
					"{2}",
					"{3}",
					{4},
					{5},
					{6},
					{7},
					{8},
					{9},
					{10},
					{11},
					{12},
					{13},
					{14},
					{15},
					{16},
					{17},
					{18},
					{19},
					{20},
					{21},
					{22},
					{23},
					{24},
					{25}
				) '''.format(\
					date,\
					float(d['strike_price']) if d['strike_price'] is not None else "null",\
					datetime.datetime.utcnow().isoformat(),\
					d['type'],\
					float(price) if price is not None else "null",\
					float(d['bid_price']) if d['bid_price'] is not None else "null",\
					float(d['ask_price']) if d['ask_price'] is not None else "null",\
					d['bid_size'],\
					d['ask_size'],\
					float(d['low_price']) if d['low_price'] is not None else "null",\
					float(d['high_price']) if d['high_price'] is not None else "null",\
					float(d['adjusted_mark_price']) if d['adjusted_mark_price'] is not None else "null",\
					d['open_interest'],\
					d['volume'],\
					float(d['chance_of_profit_long']) if d['chance_of_profit_long'] is not None else "null",\
					float(d['chance_of_profit_short']) if d['chance_of_profit_short'] is not None else "null",\
					float(d['delta']) if d['delta'] is not None else "null",\
					float(d['gamma']) if d['gamma'] is not None else "null",\
					float(d['rho']) if d['rho'] is not None else "null",\
					float(d['theta']) if d['theta'] is not None else "null",\
					float(d['vega']) if d['vega'] is not None else "null",\
					float(d['implied_volatility']) if d['implied_volatility'] is not None else "null",\
					float(d['high_fill_rate_buy_price']) if d['high_fill_rate_buy_price'] is not None else "null",\
					float(d['high_fill_rate_sell_price']) if d['high_fill_rate_sell_price'] is not None else "null",\
					float(d['low_fill_rate_buy_price']) if d['low_fill_rate_buy_price'] is not None else "null",\
					float(d['low_fill_rate_sell_price']) if d['low_fill_rate_sell_price'] is not None else "null"\
				)
			command = ' '.join(string.split())
			try:
				c.execute(command)
			except Exception as e:
				message = "Failed to insert into {0}, {1} ---- {2}".format(date, stock, datetime.datetime.utcnow())
				print(message)
				logging.warning(message+'\n'+str(e))
	conn.commit()
	conn.close()

def watch(stocks, interval): # interval in seconds, float
	start_time = datetime.datetime.utcnow()
	start_time = start_time - datetime.timedelta(seconds=interval)
	end_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
	open_time = datetime.datetime(year=start_time.year, month=start_time.month, day=start_time.day,\
			hour=13, minute=30)
	open_time = open_time - datetime.timedelta(seconds=interval)
	close_time = datetime.datetime(year=start_time.year, month=start_time.month, day=start_time.day,\
			hour=20, minute=0)
	#close_time = close_time - datetime.timedelta(seconds=interval)
	while (start_time >= open_time and start_time <= close_time):
		if (end_time - start_time).total_seconds() >= interval:
			for stock in stocks:
				getData(stock)
			start_time = start_time + datetime.timedelta(seconds=interval)
			print(start_time)
		end_time = datetime.datetime.utcnow()
		sleep(random.randint(2,10))


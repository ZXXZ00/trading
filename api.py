from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from os.path import expanduser

symbols = set(['XLK', 'XLE', 'IGM']+['TSLA', 'SNAP', 'DIS', 'BAC', 'LUV', 'WMT']+['AMZN', 'CSCO', 'NVDA', 'FB', 'F', 'AMC', 'IBM', 'WFC', 'SBUX', 'C    ', 'NFLX', 'GE', 'CVS', 'MSFT', 'AMD', 'BA', 'COST', 'XOM', 'DAL', 'CVX', 'I    NTC', 'SPY', 'UAL', 'LYFT', 'UBER', 'GOOGL', 'TWTR', 'AAL', 'JPM', 'AAPL'])
entries = ['strike_price', 'update_time', 'type', 'underlying_price', 'bid_price', 'ask_price', 'bid_size', 'ask_size', 'low_price', 'high_price', 'mark_price', 'open_interest', 'volume', 'chance_of_profit_long', 'chance_of_profit_short', 'delta', 'gamma', 'rho', 'theta', 'vega', 'implied_volatility', 'high_fill_rate_buy_price', 'high_fill_rate_sell_price', 'low_fill_rate_buy_price', 'low_fill_rate_sell_price']
path = expanduser('~')+'/trading/data/'
app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True

@app.route('/', methods=['GET'])
def home():
	return "<h1>Hello World!</h1>"

@app.route('/data', methods=['GET'])
def api_filter():
	if 'symbol' not in request.args:
		return 'symbol required'
	if 'expiration_date' not in request.args:
		return 'expiration_date required'

	symbol = request.args['symbol']
	if symbol not in symbols:
		return 'symbol not found'

	conn = sqlite3.connect(path+symbol+'.db')
	c = conn.cursor()
	exp_date = request.args['expiration_date']
	c.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="'+exp_date+'"')
	if c.fetchone() == None:
		conn.close()
		return 'invalid expiration_date'

	strike_price = request.args['strike_price']
	c.execute('SELECT strike_price FROM "'+exp_date+'" WHERE strike_price='+strike_price)
	if c.fetchone() == None:
		conn.close()
		return 'invalid strike_price'

	if 'type' not in request.args:
		return 'type required'
	option_type = request.args['type']
	if 'fileds' not in request.args:
		d = {}
		for e in entries: 
			if e == 'update_time' or e == 'type' or e == 'strike_price':
				continue
			d[e] = []
		times = []
		c.execute('SELECT * FROM "'+exp_date+'" WHERE strike_price='+strike_price+' AND type="'+option_type+'"')
		datas = c.fetchall()
		limit = range(len(entries))
		for data in datas:
			for i in limit:
				if entries[i] == 'update_time':
					times.append(data[i])
				elif not (entries[i] == 'type' or entries[i] == 'strike_price'):
					d[entries[i]].append(data[i])
		conn.close()
		l = []
		for key, val in d.items():
			item = {'field': key, 'data': val}
			l.append(item)
		ret = {'time': times, 'data': l}
		return ret

	fields = request.args['fileds'].split(' ')

	conn.close()
	return str(exp_date)
app.run()

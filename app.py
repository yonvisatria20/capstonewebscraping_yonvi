from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url = 'https://www.coingecko.com/en/coins/ethereum/historical_data/?start_date=2020-01-01&end_date=2021-06-30#panel'
url_get = requests.get(url,
                      headers = {
        'User-Agent': 'Popular browser\'s user-agent'})
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
rightkey = soup.find_all('th',class_ = 'font-semibold text-center')
row = len(rightkey)

temp = [] #initiating a list 
for tr in soup.find_all('tr')[1:]:
	ths = tr.find_all('th')
	date = ths[0].text
	tds = tr.find_all('td')
	volume = tds[1].text.strip()

	temp.append((date,volume))

temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns =('Date', 'Volume'))

#insert data wrangling here
df['Volume'] = df['Volume'].str.replace(',' , '')
df['Volume'] = df['Volume'].str.replace('$', '')
df['Volume'] = df['Volume'].astype('int64')
df['Date'] =   df['Date'].astype('datetime64')

#end of data wrangling

@app.route("/")
def index(): 
	
	card_data = f'{df["Volume"].mean()}' #be careful with the " and '

	# generate plot
	ax = df.plot(figsize = (20,9))
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
	app.run(debug=True)
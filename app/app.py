from flask import Flask, render_template, request, redirect
try: import simplejson as json
except ImportError: import json
import datetime
import requests
import pandas
import io
import bokeh
#from bokeh.plotting import figure
#from bokeh.resources import CDN
#from bokeh.embed import file_html


app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('input_page.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    return processed_text

# accepts a stock ticker input from the user and plots closing price data for the last month
ticker = 'FB'
today = datetime.date.today()
firstdaythismonth = today.replace(day=1)
lastdaylastmonth = firstdaythismonth - datetime.timedelta(days=1)
onemonthago = lastdaylastmonth.replace(day=today.day)

payload = {'start_date' : onemonthago, 'end_date': today, 'api_key': 'HZpg_ZpjP46cpex3eccE'}
r = requests.get('https://www.quandl.com/api/v3/datasets/WIKI/' + ticker + '/data.csv', params=payload)
df = pandas.read_csv(io.StringIO(r.text))

#plot = bokeh.plotting.figure()
#plot.circle([1,2], [3,4])
#htmlpage = bokeh.embed.file_html(plot, bokeh.resources.CDN, "my plot")

#@app.route('/')
#def index():
#  return render_template('index.html')



if __name__ == '__main__':
  app.run(port=33507)
  app.debug = True

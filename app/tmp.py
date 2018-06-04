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


ticker = 'FB'
today = datetime.date(2018,1,1) #datetime.date.today()
firstdaythismonth = today.replace(day=1)
lastdaylastmonth = firstdaythismonth - datetime.timedelta(days=1)
onemonthago = lastdaylastmonth.replace(day=today.day)

payload = {'start_date' : onemonthago, 'end_date': today, 'api_key': 'HZpg_ZpjP46cpex3eccE'}
r = requests.get('https://www.quandl.com/api/v3/datasets/WIKI/' + ticker + '/data.csv', params=payload)
df = pandas.read_csv(io.StringIO(r.text))


plot = bokeh.plotting.figure()
plot.circle([1,2], [3,4])
html = bokeh.embed.file_html(plot, bokeh.resources.CDN, "my plot")

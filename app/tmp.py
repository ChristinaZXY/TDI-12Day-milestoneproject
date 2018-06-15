# this file contains part of the code in app.py for debugging purpose

from flask import Flask, render_template, request, redirect, flash, url_for
from wtforms.widgets import ListWidget, CheckboxInput
from flask_debugtoolbar import DebugToolbarExtension
try: import simplejson as json
except ImportError: import json
import datetime
import requests
import pandas
import io
#import bokeh
from bokeh.plotting import figure, output_file, show
from bokeh.resources import CDN
from bokeh.embed import components
from wtforms import validators, StringField, BooleanField, SubmitField, widgets, SelectMultipleField
from flask_wtf import FlaskForm, CSRFProtect
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from flask_bootstrap import Bootstrap

import quandl

today = datetime.date(2018,2,1) #datetime.date.today()
firstdaythismonth = today.replace(day=1)
lastdaylastmonth = firstdaythismonth - datetime.timedelta(days=1)
onemonthago = lastdaylastmonth.replace(day=today.day)

#payload = {'start_date': onemonthago, 'end_date': today, 'api_key': 'HZpg_ZpjP46cpex3eccE'}
#r = requests.get('https://www.quandl.com/api/v3/datasets/EOD/HD', params=payload)
#df = pandas.read_json(io.StringIO(r.text))#, parse_dates=['Date'])

#ticker='FB'
#quandl.ApiConfig.api_key = 'HZpg_ZpjP46cpex3eccE'
#mydata = quandl.get('EOD/' + ticker, start_date=onemonthago, end_date=today)

ticker='FB'
interval_seconds = 86400
num_days = 30

payload = {'q': ticker, 'i': interval_seconds, 'p': str(num_days) + 'd', 'start_date': onemonthago, 'end_date': today, 'api_key': 'HZpg_ZpjP46cpex3eccE'}
r = requests.get('http://www.google.com/finance/getprices', params=payload)

df = pandas.read_csv(io.StringIO(r.text), skiprows=7, sep=',', names=['Date', 'Close', 'High', 'Low', 'Open', 'Volume'])
df = df[df.Date != 'TIMEZONE_OFFSET=-240']
b_dateround = df['Date'].map(lambda dt: dt[0]=='a')
dateround = df[b_dateround]['Date'].map(lambda dt: int(dt[1:]))
df['DATE2'] = dateround
df['DATE2'] = df['DATE2'].fillna(method='ffill')
df['DATE3'] = df[~b_dateround]['Date'].astype(int)*interval_seconds
df['DATE3'] = df['DATE3'].fillna(0)
df['DATE4'] = df['DATE2'] + df['DATE3']
df['DATE4'] = df['DATE4'].map(lambda s: datetime.datetime.utcfromtimestamp(int(s)))
del df['Date']
del df['DATE2']
del df['DATE3']
df = df.set_index('DATE4', verify_integrity=True)
df.index.name = 'Date'

p = figure(x_axis_type="datetime", plot_width=700, plot_height=500)
# p.line(x=df['Date'], y=df['Close'])

lines=['Close', 'Open']
colors = {'Close':'navy', 'Adj. Close': 'powderblue', 'Open': 'firebrick', 'Adj. Open':'salmon'}
p = figure(x_axis_type="datetime", plot_width=700, plot_height=500)
for line in lines:
    p.line(x=df.index, y=df[line], color=colors[line])

#p.title='Quandldata'
output_file('tmp_plot.html')
show(p)

#plot = figure()
#plot.line(x=df.Date, y=df.Close)
# htmlpage = bokeh.embed.file_html(plot, bokeh.resources.CDN, "my plot")


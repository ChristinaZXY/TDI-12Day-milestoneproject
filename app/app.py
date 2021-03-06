from flask import Flask, render_template, request, redirect, flash, url_for
from flask_debugtoolbar import DebugToolbarExtension
try: import simplejson as json
except ImportError: import json
import datetime
from calendar import monthrange
import requests
import pandas
import io
import os
from bokeh.plotting import figure, output_file, show
from bokeh.resources import CDN
from bokeh.embed import components
from wtforms import validators, StringField, BooleanField, SubmitField, widgets, SelectMultipleField
from flask_wtf import FlaskForm
from flask_nav import Nav
from flask_bootstrap import Bootstrap

app = Flask(__name__)
#app.config.from_object(__name__)
#app.debug = True
app.config['SECRET_KEY'] = 'webSafetyPurpose'
Bootstrap(app)
nav = Nav(app)
#toolbar = DebugToolbarExtension(app)

class inputForm(FlaskForm):
    ticker = StringField('ticker', validators=[validators.required()])
    year = StringField('year', validators=[validators.required()])
    month = StringField('month', validators=[validators.required()])
    line1 = BooleanField('line1')
    line2 = BooleanField('line2')
    line3 = BooleanField('line3')
    line4 = BooleanField('line4')

@app.route('/')
def index():
    form = inputForm()
    return render_template('input_page.html', form=form)

@app.route('/graph', methods=['POST'])
def graph():

    ticker = request.form.get('ticker')
    year = request.form.get('year')
    month = request.form.get('month')
    line1 = request.form.get('line1')
    line2 = request.form.get('line2')
    line3 = request.form.get('line3')
    line4 = request.form.get('line4')

    ticker = ticker.upper()
    year = int(year)
    month = int(month)
    lines = []
    if line1:
        lines.append('Close')
    if line2:
        lines.append('Adj. Close')
    if line3:
        lines.append('Open')
    if line4:
        lines.append('Adj. Open')


    datestart = datetime.date(year, month, 1)
    dateend = datetime.date(year, month, monthrange(year, month)[1])

    api_key = os.environ.get('API_key_Quandl')
    payload = {'start_date': datestart, 'end_date': dateend, 'api_key': api_key}
    r = requests.get('https://www.quandl.com/api/v3/datasets/WIKI/' + ticker + '/data.csv', params=payload)
    df = pandas.read_csv(io.StringIO(r.text), parse_dates=['Date'])

    Colors = {'Close': 'navy', 'Adj. Close': 'cyan', 'Open': 'firebrick', 'Adj. Open': 'salmon'}
    p = figure(x_axis_type="datetime", plot_width=800, plot_height=500)

    for line in lines:
        p.line(x=df['Date'], y=df[line], color=Colors[line], legend=line, line_width=2)
    p.title.text = 'Quandl WIKI Stock Prices - selected month (interactive legends: click to hide)'
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"
    p.xaxis.axis_label = 'Date [m/d]'
    p.yaxis.axis_label = 'Daily stock price [$]'

    script1, div1 = components(p)
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files[0]

    return render_template('output_page.html', script1=script1, div1=div1, cdn_css=cdn_css, cdn_js=cdn_js, template="Flask")

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0')


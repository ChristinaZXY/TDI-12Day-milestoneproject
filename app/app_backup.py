# app.py version before keeping the API key secret.  Also changed the redirect method to make a GET request directly from the frontend to this graph page.
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

@app.route('/', methods=['POST','GET'])
def index():
    form = inputForm()

    if form.validate_on_submit():
        ticker = form.ticker.data
        ticker = ticker.upper()
        year = form.year.data
        month = form.month.data
        lines = []
        if form.line1.data:
            lines.append('Close')
        if form.line2.data:
            lines.append('Adj. Close')
        if form.line3.data:
            lines.append('Open')
        if form.line4.data:
            lines.append('Adj. Open')
        return redirect(url_for('graph', ticker=ticker, year=year, month=month, lines=lines))
    else:
        print(form.errors)

    return render_template('input_page.html', form=form)


@app.route('/graph/<ticker>/<year>/<month>/<lines>') # /<ticker>/<year>/<month>/<lines>
def graph(ticker, year, month, lines): # ticker, year, month, lines

    # ticker = request.args.get('ticker')
    # year = int(request.args.get('year'))
    # month = int(request.args.get('month'))
    # lines = request.args.get('lines')

    # today = datetime.date.today()
    # firstdaythismonth = today.replace(day=1)
    # lastdaylastmonth = firstdaythismonth - datetime.timedelta(days=1)
    # onemonthago = lastdaylastmonth.replace(day=today.day)

    year = int(year)
    month = int(month)
    datestart = datetime.date(year, month, 1)
    dateend = datetime.date(year, month, monthrange(year, month)[1])

    api_key = os.environ.get('API_key_Quandl')
    payload = {'start_date': datestart, 'end_date': dateend, 'api_key': api_key}
    r = requests.get('https://www.quandl.com/api/v3/datasets/WIKI/' + ticker + '/data.csv', params=payload)
    df = pandas.read_csv(io.StringIO(r.text), parse_dates=['Date'])

    Colors = {'Close': 'navy', 'Adj. Close': 'cyan', 'Open': 'firebrick', 'Adj. Open': 'salmon'}
    p = figure(x_axis_type="datetime", plot_width=800, plot_height=500)
    lines = eval(lines) # convert the string form of a list back to a list
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


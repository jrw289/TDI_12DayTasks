from flask import Flask, render_template, request
from jinja2 import Template

import pandas as pd
import numpy as np

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models.tools import HoverTool
from bokeh.resources import INLINE

import requests

#This is James Welch's Flask-on-Heroku app for stock ticker price graphing

#Rather than adding the check mark graph selection, I included the Hovertool
#   to explore a different method and learn to use functionality for my 
#   capstone project 

app = Flask(__name__)

params =  {
           'api_key':'A5x6FwZFmGmosJH7F5e7',
           'start_date':'2017-07-01',
           'end_date':'2017-07-31',
           'order':'asc'
           }


#Page for plotting the graph
chart_page = Template('''<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Bokeh Scatter Plots</title>
        {{ resources }}
        {{ script }}
        <style>
            .embed-wrapper {
                display: flex;
                justify-content: space-evenly;
            }
        </style>
    </head>
    <body>
        <div class="embed-wrapper">
         {{ div | safe }}
        </div>
    </body>
</html>
''')

#Used to convert the dates to a Datetime array and force me to understand how to
#   include extra pacakages to understand how to include them
def datetime(x):
    return np.array(x, dtype=np.datetime64)

#Generates the Bokeh model, then returns the relevant HTML-formatted code
#   to allow plotting
def make_plot(temp_ticker):

    url_req = "https://www.quandl.com/api/v3/datasets/WIKI/%s/data.json" % temp_ticker
    r = requests.get(url_req, params=params)

    z = r.json()
    
    x = z['dataset_data']['column_names']
    y = pd.DataFrame(z['dataset_data']['data'])
    y.columns = x
    
    temp_data = pd.DataFrame(y[['Date','Close']])

    p = figure(x_axis_label='Date',
               x_axis_type='datetime',
               y_axis_label='Closing Price',
               title=('Closing Prices of ' + temp_ticker),
               plot_width=400, 
               plot_height=400
               )
     
    x = datetime(list(temp_data['Date']))
    y = list(temp_data['Close'].values)

    p.add_tools(
        HoverTool(
                   tooltips = [
                        ('date','@x{%F}'),
                        ('price','$@y')
                        ],
                
                    formatters = {
                        'x':'datetime',
                        },
                        
                        mode = 'vline'
                        ))

    p.line(x=x,y=y)

    source, div = components(p)
    resources = INLINE.render()
    
    return source, div, resources
    
#Home call to grab init_
@app.route('/',methods=['GET'])
def index():
    if request.method == 'GET':
        #return init_page.render()
        return render_template('home.html')

#Chart call and plot 
@app.route('/chart',methods=['POST'])
def chart():
    if request.method == 'POST':
        s,d,r = make_plot(request.form['ticker_name'])
        return chart_page.render(resources=r,source=s,div=d)
        #return render_template('chart.html',script=s,div=d)
        #return render_template('chart.html',resources=r,script=s,div=d)

if __name__ == '__main__':
  app.run()
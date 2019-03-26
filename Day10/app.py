from flask import Flask, render_template, request
from jinja2 import Template

import pandas as pd
import numpy as np

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models.tools import HoverTool
from bokeh.resources import INLINE

#This is James Welch's Flask-on-Heroku app for stock ticker price graphing

#I chose to include the template of the HTML I wanted to display
#   to try to see a different format than templates as well as
#   include all the code in a single place 

#Rather than adding the check mark graph selection, I included the Hovertool
#   to explore a different method and learn to use functionality for my 
#   capstone projject

app = Flask(__name__)


#Page for inputting the stock ticker
init_page = Template("""
<!doctype html>
<title>Jake's Stock Grapher</title>
<div class=page>
  <h1>Jake's Stock Grapher</h1>
  <div class=metanav>

<h4><div align="center">
The value of the stock for July 2017 will be plotted.
</div></h4>

<form id='userinfoform_lulu' method='post' action='chart' ><div align="center"> <!-- action is the URL you want to move to next-->
   <p>
   Stock Ticker: <input type='text' name='ticker_name' />
   </p>
   <p>
   <input type='Submit' value='Submit' /> <!-- value is the text that will appear on the button. -->
   </p>
</div></form>

</div>
</div>
""")


#Page for plotting the graph
template = Template('''<!DOCTYPE html>
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

#The total data set of WIKI/PRICES from Quandl was downloaded, but is quite large
#The July 2017 subset was taken instead to demonstrate functionality without
#   introducing long loading times 
data = pd.read_csv('WIKI_PRICES_JULY_2017.csv')

#Used to convert the dates to a Datetime array and force me to understand how to
#   include extra pacakages
def datetime(x):
    return np.array(x, dtype=np.datetime64)

#Generates the Bokeh model, then returns the relevant HTML-formatted code
#   to allow plotting
def make_plot(temp_ticker):

    temp_data = data[data.ticker == temp_ticker]

    p = figure(x_axis_label='Date',
               x_axis_type='datetime',
               y_axis_label='Closing Price',
               title=('Closing Prices of ' + temp_ticker),
               plot_width=400, 
               plot_height=400
               )
     
    x = datetime(list(temp_data['date']))
    y = list(temp_data['close'].values)

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
        return init_page.render()
        #return render_template('userinfo_lulu.html')

#Chart call and plot 
@app.route('/chart',methods=['POST'])
def chart():
    if request.method == 'POST':
        s,d,r = make_plot(request.form['ticker_name'])
        return template.render(resources=r,script=s,div=d)


if __name__ == '__main__':
  app.run()

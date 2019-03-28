# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 12:26:19 2019

@author: Jake Welch
"""

from flask import Flask, render_template, request
from jinja2 import Template

import pandas as pd
import numpy as np

from bokeh.embed import components
from bokeh.plotting import figure, show
from bokeh.models.tools import HoverTool
from bokeh.resources import INLINE

import requests


params =  {
           'api_key':'A5x6FwZFmGmosJH7F5e7',
           'start_date':'2017-07-01',
           'end_date':'2017-07-31',
           'order':'asc'
           }


def datetime(x):
    return np.array(x, dtype=np.datetime64)

def plotGraph(temp_ticker):
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
    
    show(p)
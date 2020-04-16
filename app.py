
import datetime as dt
import pandas as pd

import pandas_datareader as pdr
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output,Input,State
from dateutil.relativedelta import relativedelta
import plotly.graph_objs as go
from datetime import datetime

import yfinance as yf


df1 = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")



app = dash.Dash( )

app.layout = html.Div([
    html.Div(html.H1(children="Stock Dash")),

    html.Div([
        html.H4('Enter Stock Ticker:'),
        dcc.Input(id="stock-input",value="ABT",type="text"),

    ]),
   html.Div([
        html.H4('Select start and end dates:'),
        dcc.DatePickerRange(
            id='my_date_picker',
            min_date_allowed=dt.datetime(2015, 1, 1),
            max_date_allowed=dt.datetime.today(),
            start_date=dt.datetime(2018, 1, 1),
            end_date=dt.datetime.today()
        )
    ], style={'display':'inline-block'}),

    html.Div([

        html.Button(id="submit-button",children="submit",n_clicks=0)
    ]),
    html.Div([dcc.Graph(
            id="Close_Chart"
            )],className="firstcolumn"),


])
@app.callback(Output("Close_Chart","figure"),
              [Input("submit-button","n_clicks")],
              [State("stock-input","value"),
               State('my_date_picker', 'start_date'),
               State('my_date_picker', 'end_date')]
              )

def update_fig(n_clicks,input_value,start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    df = pdr.DataReader(input_value, 'yahoo', start, end)
    data=[]
    trace_close = go.Scatter(x=list(df.index),
                             y=list(df.Close),
                             name="Close",
                             line=dict(color="blue")
                            )
    data.append(trace_close)
    layout = dict(title=input_value + " Stock Chart",
                  showlegend=True)
    fig = dict(data=data, layout=layout)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

# link: http://127.0.0.1:8050/

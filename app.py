import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import bs4 as bs
import requests

# Import External Stylesheets from Materialize CSS
external_css = [open('stylesheets.txt', 'r').read()]

# Define Slugs from Yahoo Finance SG
INDEX_SLUGS = {
    'Dow Jones Index': '%5EDJI',
    'FTSE 100 Index': '%5EFTSE',
    'NASDAQ Index': '%5EIXIC',
    'DAX Index': '%5EGDAXI',
    'Straits Times Index': '%5ESTI',
    'Hang Seng Index': '%5EHSI',
}


def load_constituents(market_index):
    # Parse Yahoo Finance for Constituent Stocks Per Market Index
    resp = requests.get(
        f'https://sg.finance.yahoo.com/quote/{INDEX_SLUGS[market_index]}/components?p={INDEX_SLUGS[market_index]}')
    soup = bs.BeautifulSoup(resp.text, features='lxml')
    table = soup.find(
        'table', attrs={'class': 'W(100%) M(0) BdB Bdc($finLightGray)'})
    tickers = {}

    for row in table.findAll('tr')[1:]:
        name = row.findAll('td')[1].text
        ticker = row.findAll('td')[0].text
        tickers[name] = ticker

    # Sort the Dictionary of Stock Name-Stock Ticker Items
    sorted_tickers = {}

    for key, value in sorted(tickers.items()):
        sorted_tickers[key] = value

    return sorted_tickers


# Initialise the App and Define the App Layout
app = dash.Dash(__name__, external_stylesheets=external_css)

app.layout = html.Div(

    children=[

        # Header
        html.H2(
            style={"textAlign": "center"},
            children='Equity Market Visualisation Dashboard'),

        # Row Div
        html.Div(
            style={
                'padding-top': '100',
                'display': 'inline-block',
                "height": "100%",
                "width": "100%",
            },
            children=[

                # Column 1 Div
                html.Div(
                    style={
                        'width': '45%',
                        'display': 'inline-block',
                        "margin": "0px 0px 0px 50px", },
                    children=[
                        html.Label('Select an Index'),
                        dcc.Dropdown(
                            id='index-dropdown-1',
                            options=[{'label': i, 'value': i}
                                     for i in INDEX_SLUGS.keys()],
                            value='Dow Jones Index',
                        ),
                        html.Label(
                            'Select an Index Constituent to Visualise: '),
                        dcc.Dropdown(
                            id='constituent-dropdown-1',
                            value='MMM'
                        ),
                        html.H5('\n'),
                        html.Output(
                            id='graph-1',)
                    ]
                ),

                # Column 2 Div
                html.Div(
                    style={
                        'width': '45%',
                        'display': 'inline-block',
                        "margin": "0px 0px 0px 50px", },
                    children=[
                        html.Label('Select an Index'),
                        dcc.Dropdown(
                            id='index-dropdown-2',
                            options=[{'label': i, 'value': i}
                                     for i in INDEX_SLUGS.keys()],
                            value='FTSE 100 Index',
                        ),
                        html.Label(
                            'Select an Index Constituent to Visualise: '),
                        dcc.Dropdown(
                            id='constituent-dropdown-2',
                            value='ANTO.L'
                        ),
                        html.H5('\n'),
                        html.Output(
                            id='graph-2')
                    ]
                )
            ])
    ])

# Generate Callbacks between Market Index-Constituents and Constituent-Yahoo Finance API
for col in range(2):

    graph_index = col + 1

    # Populate Constituents Dropdown List based on Market Index selected
    @app.callback(
        Output(
            component_id=f"constituent-dropdown-{graph_index}", component_property='options'),
        [Input(
            component_id=f"index-dropdown-{graph_index}", component_property='value')]
    )
    def populate_constituents(market_index):
        market_dict = load_constituents(market_index)
        return [{'label': i, 'value': market_dict[i]} for i in market_dict.keys()]

    # Call Yahoo Finance API based on Constituent Stock Selected

    @app.callback(
        Output(component_id=f"graph-{graph_index}",
               component_property='children'),
        [Input(component_id=f"constituent-dropdown-{graph_index}",
               component_property='value')]
    )
    def update_graph(ticker):
        start = dt.datetime(year=2000, month=1, day=1)
        end = dt.datetime.now()
        source = 'yahoo'

        df = web.DataReader(ticker, source, start, end)

        return dcc.Graph(
            style={
                "width": "100%",
                "height": "100%"
            },
            figure={
                'data': [
                    {'x': df.index, 'y': df['Adj Close'],
                        'type': 'line', 'name': 'Price'},
                    {'x': df.index, 'y': df['Volume'], 'type': 'bar',
                        'name': 'Volume', 'yaxis': 'y2', 'opacity': 0.25},
                ],
                'layout': go.Layout(
                    showlegend=False,
                    title=f'{ticker} Stock Price and Volume',
                    yaxis=dict(
                        title='Price'
                    ),
                    yaxis2=dict(
                        title='Volume',
                        overlaying='y',
                        side='right',
                    ),
                )
            }
        )


if __name__ == '__main__':
    app.run_server(debug=True)

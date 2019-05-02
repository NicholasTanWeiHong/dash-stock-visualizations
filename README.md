# dash-stock-visualizations
This is a visualization framework for stocks written with the Dash Framework by [Plotly](https://plot.ly/).

## Using the App
The app uses the requests and BeautifulSoup4 libraries to parse [Yahoo Finance](https://sg.finance.yahoo.com/) based on pre-determined slugs.

Given a selected Market Index, it uses Dash Callbacks to populate a second Dropdown List with all constituent stocks in the given Market.

Finally, it plots Historical Price and Volume based on a pandas DataFrame which is returned from the Yahoo Finance API.
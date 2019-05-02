# dash-stock-visualizations
This is a visualization framework for stocks written with the Dash Framework by [Plotly](https://plot.ly/).

![App Screenshot](https://github.com/NicholasTanWeiHong/dash-stock-visualizations/blob/master/images/screenshot.PNG "App Screenshot")

## Using the App
The app uses the [requests](https://realpython.com/python-requests/) and [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) libraries to parse [Yahoo Finance](https://sg.finance.yahoo.com/) based on pre-determined slugs.

Given a selected Market Index, it uses Dash Callbacks to populate a second Dropdown List with all constituent stocks in the given Market.

Finally, it plots Historical Price and Volume based on a pandas DataFrame which is returned from the Yahoo Finance API.

## Future Plans
* Integrate [DatePickerSingle Components](https://dash.plot.ly/dash-core-components/datepickersingle) from Dash to filter data by time
* Implement additional functions for Technical Analysis (E.g. RSI, MACD, Bollinger Bands)
* Implement the option to overlay price charts of two stocks on the same graph
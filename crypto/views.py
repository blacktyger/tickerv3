from django.shortcuts import render
import json
import requests
from .utils import *
import timeago, datetime

def home(request):

    now = datetime.datetime.now() + datetime.timedelta(seconds=60 * 3.4)
    date = datetime.datetime.now()

    api_request = requests.get("https://api.coingecko.com/api/v3/coins/epic-cash/")
    api_ticker = json.loads(api_request.content)

    api_request_epic_usd = requests.get(
        "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=epic-cash&order=market_cap_desc&per_page=100&page=1&sparkline=true&price_change_percentage=24h%2C7d")
    api_epic_usd = json.loads(api_request_epic_usd.content)

    api_request_epic_btc = requests.get(
        "https://api.coingecko.com/api/v3/coins/markets?vs_currency=btc&ids=epic-cash&order=market_cap_desc&per_page=100&page=1&sparkline=true&price_change_percentage=24h%2C7d")
    api_epic_btc = json.loads(api_request_epic_btc.content)

    api_request_vol_usd = requests.get("https://api.coingecko.com/api/v3/coins/epic-cash/market_chart?vs_currency=usd&days=1")
    api_vol_usd = json.loads(api_request_vol_usd.content)


    def arrow_check_price7dbtc():
        for x in api_epic_btc:
            if x['price_change_percentage_7d_in_currency'] < 0:
                return '<i class="material-icons text-danger">call_received</i>'
            else:
                return '<i class="material-icons text-success">call_made</i>'

    def arrow_check_price24btc():
        for x in api_epic_btc:
            if x['price_change_24h'] < 0:
                return '<i class="material-icons text-danger">call_received</i>'
            else:
                return '<i class="material-icons text-success">call_made</i>'

    def arrow_check_capbtc():
        for x in api_epic_btc:
            if x['market_cap_change_24h'] < 0:
                return '<i class="material-icons text-danger">call_received</i>'
            else:
                return '<i class="material-icons text-success">call_made</i>'

    def arrow_check_price7d():
        for x in api_epic_usd:
            if x['price_change_percentage_7d_in_currency'] < 0:
                return '<i class="material-icons text-danger">call_received</i>'
            else:
                return '<i class="material-icons text-success">call_made</i>'

    def arrow_check_price24():
        for x in api_epic_usd:
            if x['price_change_24h'] < 0:
                return '<i class="material-icons text-danger">call_received</i>'
            else:
                return '<i class="material-icons text-success">call_made</i>'

    def arrow_check_cap():
        for x in api_epic_usd:
            if x['market_cap_change_24h'] < 0:
                return '<i class="material-icons text-danger">call_received</i>'
            else:
                return '<i class="material-icons text-success">call_made</i>'


    ctx = {

        'now': now,
        'date': date,

        'api_vol_usd': api_vol_usd,
        'arrow_check_capbtc': arrow_check_capbtc(),
        'arrow_check_price24btc': arrow_check_price24btc(),
        'arrow_check_price7dbtc': arrow_check_price7dbtc(),
        'arrow_check_cap': arrow_check_cap(),
        'arrow_check_price24': arrow_check_price24(),
        'arrow_check_price7d': arrow_check_price7d(),

        'api_ticker': api_ticker,
        'api_epic_btc': api_epic_btc,
        'api_epic_usd': api_epic_usd,
        'api_bihodl_usd': api_bihodl_usd(),
        'api_citex_usd': api_citex_usd(),
        'api_citex_btc': api_citex_btc(),
        'api_chainrift_btc': api_chainrift_btc(),
        'fapi_epic_usd': fapi_epic_usd(),
        'fapi_epic_btc': fapi_epic_btc(),
    }

    return render(request, 'home.html', ctx)

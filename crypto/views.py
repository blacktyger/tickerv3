from django.shortcuts import render
import json
import requests
from django import template
from django.template.defaulttags import register
from django.http import HttpResponse, HttpResponseNotFound, Http404,  HttpResponseRedirect
import timeago
import datetime
import os.path





def home(request):

    now = datetime.datetime.now() + datetime.timedelta(seconds=60 * 3.4)
    date = datetime.datetime.now()

    @register.filter(name='vol_supply')
    def vol_supply(value):
        for vol in api_ticker['tickers']:
            if vol['market']['identifier'] == "citex" and vol['target'] == 'USDT':
                vol1 = vol['volume']
        for vol in api_ticker['tickers']:
            if vol['market']['identifier'] == "bihodl" and vol['target'] == 'USDT':
                vol2 = vol['volume']
        vol_total = vol1 + vol2
        epic_vol = vol_total
        percent = (epic_vol/float(value))*100
        return float(percent)

    @register.filter('last_trade')
    def last_trade(value):
        value = str(value)
        new_value = value[0:10] + " " + value[11:19]
        return timeago.format(new_value, now)

    api_request = requests.get(
        "https://api.coingecko.com/api/v3/coins/epic-cash/")
    api_ticker = json.loads(api_request.content)

    api_request_btc = requests.get(
        "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
    api_btc = json.loads(api_request_btc.content)

    api_request_epic_usd = requests.get(
        "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=epic-cash&order=market_cap_desc&per_page=100&page=1&sparkline=true&price_change_percentage=24h%2C7d")
    api_epic_usd = json.loads(api_request_epic_usd.content)

    api_request_epic_btc = requests.get(
        "https://api.coingecko.com/api/v3/coins/markets?vs_currency=btc&ids=epic-cash&order=market_cap_desc&per_page=100&page=1&sparkline=true&price_change_percentage=24h%2C7d")
    api_epic_btc = json.loads(api_request_epic_btc.content)

    api_request_vol_usd = requests.get(
        "https://api.coingecko.com/api/v3/coins/epic-cash/market_chart?vs_currency=usd&days=1")
    api_vol_usd = json.loads(api_request_vol_usd.content)

    api_request_fast = requests.get("https://fastepic.eu/stocks")
    api_fast = json.loads(api_request_fast.content)

    def fast_spread():
        for s in api_fast['stocks']:
            bid = s['pricebid']
            ask = s['priceask']
            spread = ask - bid
            percent = (spread / ask) * 100
            return percent


    @register.filter('usdtoepic')
    def usdtoepic(value):
        for x in api_epic_usd:
            usd = x['current_price']
        epic = float(value)/usd
        return f"{int(epic)} <img style='height: 25px;' class='pb-1' src='static/images/btn1.png'>"

    @register.filter('btctousd')
    def btc_price(value):
        for k, v in api_btc.items():
            usd_price = v['usd']
            return value * usd_price

    @register.filter('usdtobtc')
    def usdtobtc(value):
        for k, v in api_btc.items():
            usd_price = v['usd']
            return value / usd_price

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

    def arrow_check_vol():
        for x in api_vol_usd['total_volumes'][0]:
           day_ago = x
        for x in api_epic_usd:
            now = x['total_volume']
        if day_ago > now:
            return '<i class="material-icons text-danger">call_received</i>'
        else:
            return '<i class="material-icons text-success">call_made</i>'

    def check_vol():
        for x in api_vol_usd['total_volumes'][0]:
           day_ago = x
        for x in api_epic_usd:
            now = x['total_volume']
        diff = now - day_ago
        procent = (now/diff) * 100
        return procent

    def arrow_check_ath():
        for x in api_epic_usd:
            if x['ath_change_percentage'] < 0:
                return '<i class="material-icons text-danger">call_received</i>'
            else:
                return '<i class="material-icons text-success">call_made</i>'

    def avg_price_usd():
        for x in api_ticker['tickers']:
            if x['target'] == "BTC":
                price_btc = btc_price(x['last'])
            if x['target'] == "USDT":
                price_usd = x['last']
        return (price_btc + price_usd)/3

    def total_vol_usd():
        for vol in api_ticker['tickers']:
            if vol['market']['identifier'] == "citex" and vol['target'] == 'USDT':
                vol1 = vol['converted_volume']['usd']
        for vol in api_ticker['tickers']:
            if vol['market']['identifier'] == "bihodl" and vol['target'] == 'USDT':
                vol2 = vol['converted_volume']['usd']
        vol_total = vol1 + vol2
        return vol_total

    def total_vol_epic():
        for vol in api_ticker['tickers']:
            if vol['market']['identifier'] == "citex" and vol['target'] == 'USDT':
                vol1 = vol['volume']
        for vol in api_ticker['tickers']:
            if vol['market']['identifier'] == "bihodl" and vol['target'] == 'USDT':
                vol2 = vol['volume']
        vol_total = vol1 + vol2
        return vol_total

    def total_vol_btc():
        for vol in api_ticker['tickers']:
            if vol['market']['identifier'] == "citex" and vol['target'] == 'BTC':
                vol1 = vol['converted_volume']['btc']
        for vol in api_fast['stocks']:
            vol2 = vol['volume24h']
        vol_total = vol1 + vol2
        return vol_total

    def total_vol():
        usd = total_vol_usd()
        btc = btc_price(total_vol_btc())
        return usd + btc

    

    ctx = {

        'fast_spread': fast_spread(),

        'now': now,
        'date': date,

        'api_vol_usd': api_vol_usd,
        'arrow_check_capbtc': arrow_check_capbtc(),
        'arrow_check_price24btc': arrow_check_price24btc(),
        'arrow_check_price7dbtc': arrow_check_price7dbtc(),
        'arrow_check_cap': arrow_check_cap(),
        'arrow_check_price24': arrow_check_price24(),
        'arrow_check_price7d': arrow_check_price7d(),
        'arrow_check_ath': arrow_check_ath(),
        'arrow_check_vol': arrow_check_vol(),

        'avg_price_usd': avg_price_usd(),
        'total_vol_usd': total_vol_usd(),
        'total_vol_btc': total_vol_btc(),
        'total_vol_epic':total_vol_epic(),
        'total_vol': total_vol(),
        'check_vol': check_vol(),

        'api_fast': api_fast,
        'api_ticker': api_ticker,
        'api_epic_btc': api_epic_btc,
        'api_epic_usd': api_epic_usd,


        'navbar': 'navbar.html',
        'footer': 'footer.html',
        'left_nav': 'left_nav.html',
        'right_nav': 'right_nav.html',
        'table_ex': 'table_ex.html',
        'table_price': 'table_price.html',
        'cards': 'cards.html',
        'fast': 'fast.html',

        'title': 'Home',
    }

    return render(request, 'home.html', ctx)


def fastepic(request):
    now = datetime.datetime.now() + datetime.timedelta(seconds=60 * 3.4)
    date = datetime.datetime.now()

    @register.filter(name='vol_supply')
    def vol_supply(value):
        for vol in api_ticker['tickers']:
            if vol['market']['identifier'] == "citex" and vol['target'] == 'USDT':
                vol1 = vol['volume']
        for vol in api_ticker['tickers']:
            if vol['market']['identifier'] == "bihodl" and vol['target'] == 'USDT':
                vol2 = vol['volume']
        vol_total = vol1 + vol2
        epic_vol = vol_total
        percent = (epic_vol/float(value))*100
        return float(percent)

    @register.filter('last_trade')
    def last_trade(value):
        value = str(value)
        new_value = value[0:10] + " " + value[11:19]
        return timeago.format(new_value, now)

    api_request = requests.get(
        "https://api.coingecko.com/api/v3/coins/epic-cash/")
    api_ticker = json.loads(api_request.content)

    api_request_btc = requests.get(
        "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
    api_btc = json.loads(api_request_btc.content)

    api_request_epic_usd = requests.get(
        "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=epic-cash&order=market_cap_desc&per_page=100&page=1&sparkline=true&price_change_percentage=24h%2C7d")
    api_epic_usd = json.loads(api_request_epic_usd.content)

    api_request_epic_btc = requests.get(
        "https://api.coingecko.com/api/v3/coins/markets?vs_currency=btc&ids=epic-cash&order=market_cap_desc&per_page=100&page=1&sparkline=true&price_change_percentage=24h%2C7d")
    api_epic_btc = json.loads(api_request_epic_btc.content)

    api_request_vol_usd = requests.get(
        "https://api.coingecko.com/api/v3/coins/epic-cash/market_chart?vs_currency=usd&days=1")
    api_vol_usd = json.loads(api_request_vol_usd.content)

    api_request_fast = requests.get("https://fastepic.eu/stocks")
    api_fast = json.loads(api_request_fast.content)

    def fast_spread():
        for s in api_fast['stocks']:
            bid = s['pricebid']
            ask = s['priceask']
            spread = ask - bid
            percent = (spread / ask) * 100
            return percent


    @register.filter('usdtoepic')
    def usdtoepic(value):
        for x in api_epic_usd:
            usd = x['current_price']
        epic = float(value)/usd
        return f"{int(epic)} <img style='height: 25px;' class='pb-1' src='static/images/btn1.png'>"

    @register.filter('btctousd')
    def btc_price(value):
        for k, v in api_btc.items():
            usd_price = v['usd']
            return value * usd_price

    @register.filter('usdtobtc')
    def usdtobtc(value):
        for k, v in api_btc.items():
            usd_price = v['usd']
            return value / usd_price

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

    def arrow_check_vol():
        for x in api_vol_usd['total_volumes'][0]:
           day_ago = x
        for x in api_epic_usd:
            now = x['total_volume']
        if day_ago > now:
            return '<i class="material-icons text-danger">call_received</i>'
        else:
            return '<i class="material-icons text-success">call_made</i>'

    def check_vol():
        for x in api_vol_usd['total_volumes'][0]:
           day_ago = x
        for x in api_epic_usd:
            now = x['total_volume']
        diff = now - day_ago
        procent = (now/diff) * 100
        return procent

    def arrow_check_ath():
        for x in api_epic_usd:
            if x['ath_change_percentage'] < 0:
                return '<i class="material-icons text-danger">call_received</i>'
            else:
                return '<i class="material-icons text-success">call_made</i>'

    def avg_price_usd():
        for x in api_ticker['tickers']:
            if x['target'] == "BTC":
                price_btc = btc_price(x['last'])
            if x['target'] == "USDT":
                price_usd = x['last']
        return (price_btc + price_usd)/3

    def total_vol_usd():
        for vol in api_ticker['tickers']:
            if vol['market']['identifier'] == "citex" and vol['target'] == 'USDT':
                vol1 = vol['converted_volume']['usd']
        for vol in api_ticker['tickers']:
            if vol['market']['identifier'] == "bihodl" and vol['target'] == 'USDT':
                vol2 = vol['converted_volume']['usd']
        vol_total = vol1 + vol2
        return vol_total

    def total_vol_epic():
        for vol in api_ticker['tickers']:
            if vol['market']['identifier'] == "citex" and vol['target'] == 'USDT':
                vol1 = vol['volume']
        for vol in api_ticker['tickers']:
            if vol['market']['identifier'] == "bihodl" and vol['target'] == 'USDT':
                vol2 = vol['volume']
        vol_total = vol1 + vol2
        return vol_total

    def total_vol_btc():
        for vol in api_ticker['tickers']:
            if vol['market']['identifier'] == "citex" and vol['target'] == 'BTC':
                vol1 = vol['converted_volume']['btc']
        for vol in api_fast['stocks']:
            vol2 = vol['volume24h']
        vol_total = vol1 + vol2
        return vol_total

    def total_vol():
        usd = total_vol_usd()
        btc = btc_price(total_vol_btc())
        return usd + btc

    
    ctx = {

        'fast_spread': fast_spread(),

        'now': now,
        'date': date,

        'api_vol_usd': api_vol_usd,
        'arrow_check_capbtc': arrow_check_capbtc(),
        'arrow_check_price24btc': arrow_check_price24btc(),
        'arrow_check_price7dbtc': arrow_check_price7dbtc(),
        'arrow_check_cap': arrow_check_cap(),
        'arrow_check_price24': arrow_check_price24(),
        'arrow_check_price7d': arrow_check_price7d(),
        'arrow_check_ath': arrow_check_ath(),
        'arrow_check_vol': arrow_check_vol(),

        'avg_price_usd': avg_price_usd(),
        'total_vol_usd': total_vol_usd(),
        'total_vol_btc': total_vol_btc(),
        'total_vol_epic':total_vol_epic(),
        'total_vol': total_vol(),
        'check_vol': check_vol(),

        'api_fast': api_fast,
        'api_ticker': api_ticker,
        'api_epic_btc': api_epic_btc,
        'api_epic_usd': api_epic_usd,

        'navbar': 'navbar.html',
        'footer': 'footer.html',
        'left_nav': 'left_nav.html',
        'right_nav': 'right_nav.html',
        'table_ex': 'table_ex.html',
        'table_price': 'table_price.html',
        'cards': 'cards.html',
        'fast': 'fast.html',
        
        'title': 'fastepic.eu',

    }

    return render(request, 'fastepic.html', ctx)
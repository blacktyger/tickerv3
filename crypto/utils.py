from django.shortcuts import render
import json
import requests


api_request = requests.get("https://api.coingecko.com/api/v3/coins/epic-cash/")
api = json.loads(api_request.content)

api_request_epic_usd = requests.get(
    "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=epic-cash&order=market_cap_desc&per_page=100&page=1&sparkline=false")
api_epic_usd = json.loads(api_request_epic_usd.content)

api_request_epic_btc = requests.get(
    "https://api.coingecko.com/api/v3/coins/markets?vs_currency=btc&ids=epic-cash&order=market_cap_desc&per_page=100&page=1&sparkline=false")
api_epic_btc = json.loads(api_request_epic_btc.content)



def datex(value):
    value = str(value)
    new_value = value[0:10]+" "+value[11:16]
    return f"{new_value} UTC"


def btc(value):
    return f"₿ {value:.8f}"

def usd2(value):
    return f"$ {value:.2f}"

def usd3(value):
    return f"$ {value:.3f}"

def procent(value):
    return f"{value:.1f} %"

def api_bihodl_usd():
    for bihodl_usd in api['tickers']:
        if bihodl_usd['market']['name'] == 'BiHODL' and bihodl_usd['target'] == "USD":
            market = bihodl_usd['market']['name']
            price = usd3(bihodl_usd['last'])
            vol24_usd = usd2(bihodl_usd['converted_volume']['usd'])
            vol24_epic = bihodl_usd['volume']
            vol24_btc = btc(bihodl_usd['converted_volume']['btc'])
            vs_currency = bihodl_usd['target']
            last_trade = datex(bihodl_usd['last_traded_at'])
            trade_url = "https://www.bihodl.com/#/exchange/epic_usdt"
            spread = procent(bihodl_usd['bid_ask_spread_percentage'])

            bihodl_usd_list = {
                'Exchange': market,
                'Last Price': price,
                'USD Volume 24h': vol24_usd,
                'EPIC Volume 24h': vol24_epic,
                'BTC Volume 24h': vol24_btc,
                'Currency': vs_currency,
                'Last Trade': last_trade,
                'trade_url': trade_url,
                'Bid / Ask Spread': spread,

            }

            return bihodl_usd_list

def api_citex_usd():
    for citex_usd in api['tickers']:
        if citex_usd['target'] == "USDT" and citex_usd['market']['name'] == "CITEX":
            market = citex_usd['market']['name']
            price = usd3(citex_usd['last'])
            vol24_usd = usd2(citex_usd['converted_volume']['usd'])
            vol24_epic = citex_usd['volume']
            vol24_btc = btc(citex_usd['converted_volume']['btc'])
            last_trade = datex(citex_usd['last_traded_at'])
            trade_url = "https://www.citex.co.kr/#/trade/EPIC_USDT"
            spread = procent(citex_usd['bid_ask_spread_percentage'])
            vs_currency = citex_usd['target']

            citex_usd_list = {
                'Exchange': market,
                'Last Price': price,
                'USD Volume 24h': vol24_usd,
                'EPIC Volume 24h': vol24_epic,
                'BTC Volume 24h': vol24_btc,
                'Currency': vs_currency,
                'Last Trade': last_trade,
                'trade_url': trade_url,
                'Bid / Ask Spread': spread,
            }

            return citex_usd_list


def api_citex_btc():
    for citex_btc in api['tickers']:
        if citex_btc['target'] == "BTC" and citex_btc['market']['name'] == "CITEX":
            market = citex_btc['market']['name']
            price = btc(citex_btc['last'])
            vol24_usd = usd2(citex_btc['converted_volume']['usd'])
            vol24_epic = citex_btc['volume']
            vol24_btc = btc(citex_btc['converted_volume']['btc'])
            last_trade = datex(citex_btc['last_traded_at'])
            trade_url = "https://www.citex.co.kr/#/trade/EPIC_BTC"
            spread = procent(citex_btc['bid_ask_spread_percentage'])
            vs_currency = citex_btc['target']

            citex_btc_list = {
                'Exchange': market,
                'Last Price': price,
                'USD Volume 24h': vol24_usd,
                'EPIC Volume 24h': vol24_epic,
                'BTC Volume 24h': vol24_btc,
                'Currency': vs_currency,
                'Last Trade': last_trade,
                'trade_url': trade_url,
                'Bid / Ask Spread': spread,
            }

            return citex_btc_list


def api_chainrift_btc():
    for chainrift_btc in api['tickers']:
        if chainrift_btc['target'] == "BTC" and chainrift_btc['market']['name'] == "Chainrift":
            market = chainrift_btc['market']['name']
            price = btc(chainrift_btc['last'])
            vol24_usd = usd2(chainrift_btc['converted_volume']['usd'])
            vol24_epic = chainrift_btc['volume']
            vol24_btc = btc(chainrift_btc['converted_volume']['btc'])
            last_trade = datex(chainrift_btc['last_traded_at'])
            trade_url = "https://www.chainrift.com/trading?coinpair=EPIC/BTC&"
            spread = procent(chainrift_btc['bid_ask_spread_percentage'])
            vs_currency = chainrift_btc['target']

            chainrift_btc_list = {
                'Exchange': market,
                'Last Price': price,
                'USD Volume 24h': vol24_usd,
                'EPIC Volume 24h': vol24_epic,
                'BTC Volume 24h': vol24_btc,
                'Currency': vs_currency,
                'Last Trade': last_trade,
                'trade_url': trade_url,
                'Bid / Ask Spread': spread,
            }

            return chainrift_btc_list

def fapi_epic_usd():
    for epic_usd in api_epic_usd:
        name = epic_usd['name']
        img = epic_usd['image']
        price = usd3(epic_usd['current_price'])
        market_cap = usd2(epic_usd['market_cap'])
        usd_vol24 = usd2(epic_usd['total_volume'])
        high24 = usd3(epic_usd['high_24h'])
        low24 = usd3(epic_usd['low_24h'])
        change24 = usd3(epic_usd['price_change_24h'])
        change24_per = procent(epic_usd['price_change_percentage_24h'])
        market_cap_change24 = usd2(epic_usd['market_cap_change_24h'])
        market_cap_change24_per = procent(epic_usd['market_cap_change_percentage_24h'])
        supply = epic_usd['circulating_supply']
        ath = usd3(epic_usd['ath'])
        ath_change24_per = procent(epic_usd['ath_change_percentage'])
        ath_date = datex(epic_usd['ath_date'])

        fapi_epic_usd_list = {
            'Coin': name,
            'img': img,
            'Price': price,
            'Market Cap': market_cap,
            'Volume 24h': usd_vol24,
            'High 24h': high24,
            'Low 24h': low24,
            'Price Change 24h': change24,
            'Price Change 24h ': change24_per,
            'Market Cap Change 24h': market_cap_change24,
            'Market Cap Change 24h ': market_cap_change24_per,
            'Total Supply': supply,
            'All Time High': ath,
            'ATH 24h Change': ath_change24_per,
            'ATH Date': ath_date,
        }


        return fapi_epic_usd_list

def fapi_epic_btc():
    for epic_btc in api_epic_btc:
        name = epic_btc['name']
        img = epic_btc['image']
        price = btc(epic_btc['current_price'])
        market_cap = btc(epic_btc['market_cap'])
        btc_vol24 = btc(epic_btc['total_volume'])
        high24 = btc(epic_btc['high_24h'])
        low24 = btc(epic_btc['low_24h'])
        change24 = btc(epic_btc['price_change_24h'])
        change24_per = procent(epic_btc['price_change_percentage_24h'])
        market_cap_change24 = btc(epic_btc['market_cap_change_24h'])
        market_cap_change24_per = procent(epic_btc['market_cap_change_percentage_24h'])
        supply = epic_btc['circulating_supply']
        ath = btc(epic_btc['ath'])
        ath_change24_per = procent(epic_btc['ath_change_percentage'])
        ath_date = datex(epic_btc['ath_date'])

        fapi_epic_btc_list = {
            'Coin': name,
            'img': img,
            'Price': price,
            'Market Cap': market_cap,
            'Volume 24h': btc_vol24,
            'High 24h': high24,
            'Low 24h': low24,
            'Price Change 24h': change24,
            'Price Change 24h ': change24_per,
            'Market Cap Change 24h': market_cap_change24,
            'Market Cap Change 24h ': market_cap_change24_per,
            'Total Supply': supply,
            'All Time High': ath,
            'ATH 24h Change': ath_change24_per,
            'ATH Date': ath_date,
        }

        return fapi_epic_btc_list




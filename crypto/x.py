import json
import requests



def petle():

    global vol24
    api_request = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=epic-cash&order=market_cap_desc&per_page=100&page=1&sparkline=false")
    api = json.loads(api_request.content)

    for key in api:
        return key

print(petle())
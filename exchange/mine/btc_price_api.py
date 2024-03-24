import requests
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response


@api_view(['GET'])
def btc_price(request):

    url = 'https://api.nobitex.ir/v2/orderbook/BTCUSDT'
    response = requests.get(url)

    res = response.json()
    price = res['lastTradePrice'] 

    return Response(price, status.HTTP_200_OK)
import requests
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response


@api_view(['GET'])
def currency_price(request, name):

    url = f'https://api.nobitex.ir/v2/orderbook/{name}'
    
    res = requests.get(url).json()
    price = res['lastTradePrice'] 

    return Response(f'{name}: {price}', status.HTTP_200_OK)
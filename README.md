
## create virtual env

python3 -m venv venv

activate the venv
python3 -m venv venv

python -m pip install Django

pip install djangorestframework
pip install djangorestframework-simplejwt
pip install django-cors-headers
pip install drf_yasg


python manage.py runserver 


django-admin startproject core .

## generate secret key

python manage.py shell

from django.core.management.utils import get_random_secret_key

## running in dev/local mode

## running in prod mode

## freezing dependencies

pip freeze > requirements.txt

pip install -r requirements.txt

## vscode settings

install black , python

###

flake8 installtion

# create new app

create a folder names mvp under onsecope/onescope

python manage.py startapp polls rsbackend/mvp

## AUTH

<https://www.youtube.com/watch?v=2kKwPk5qPUs>

For auth refer- <https://www.youtube.com/watch?v=QFDyXWRYQjY&list=PLJRGQoqpRwdfoa9591BcUS6NmMpZcvFsM&index=1>

<https://www.youtube.com/watch?v=AfYfvjP1hK8&t=2873s>

python manage.py shell

> for shell

from rsbackend.authentication.models import User
User.objects.get()
User.objects.get().tokens()

python manage.py makemigrations mvp


celery -A rsbackend worker -B  -l info

https://dev-openapi.5paisa.com/WebVendorLogin/VLogin/Index?VendorKey=Bm5Q6CrtQkGCeolRCMox0ijVKregr0u1&ResponseURL=https://f2bf-171-76-87-249.ngrok-free.app/fivep/callback


https://dev-openapi.5paisa.com/WebVendorLogin/VLogin/Index?VendorKey=Bm5Q6CrtQkGCeolRCMox0ijVKregr0u1&ResponseURL=https://a5ed-171-76-81-113.ngrok-free.app/fivep/callback/2eba0a8d-fef9-405a-9545-f6fb6c9935d3


{'CacheTime': 5, 'Exch': 'N', 'ExchType': 'C', 
'MarketDepthData': [{'BbBuySellFlag': 66, 'NumberOfOrders': 1, 'Price': 0, 'Quantity': 0}, {'BbBuySellFlag': 66, 'NumberOfOrders': 1, 'Price': 0, 'Quantity': 0}, {'BbBuySellFlag': 66, 'NumberOfOrders': 1, 'Price': 0, 'Quantity': 0}, {'BbBuySellFlag': 66, 'NumberOfOrders': 1, 'Price': 0, 'Quantity': 0}, {'BbBuySellFlag': 66, 'NumberOfOrders': 1, 'Price': 0, 'Quantity': 0}, 
{'BbBuySellFlag': 83, 'NumberOfOrders': 0, 'Price': 0, 'Quantity': 0}, {'BbBuySellFlag': 83, 'NumberOfOrders': 0, 'Price': 0, 'Quantity': 0}, {'BbBuySellFlag': 83, 'NumberOfOrders': 0, 'Price': 0, 'Quantity': 0}, {'BbBuySellFlag': 83, 'NumberOfOrders': 0, 'Price': 0, 'Quantity': 0}, {'BbBuySellFlag': 83, 'NumberOfOrders': 0, 'Price': 0, 'Quantity': 0}],

 'Message': 'Success', 'ScripCode': 999920005, 'Status': 0, 'TimeStamp': '/Date(1694007299000+0530)/'}



marekt  full 
[2023-09-06 15:31:06,722: WARNING/ForkPoolWorker-9] {'CacheTime': 0, 'Data': [{'AverageTradePrice': 0, 'BuyQuantity': 0, 'Close': '44532.15', 'Exchange': 'N', 'ExchangeType': 'C', 'High': '44577', 'LastQuantity': 0, 'LastTradeTime': '/Date(1694007299000)/', 'LastTradedPrice': 44409.1, 'Low': '44207.25', 'NetChange': '-123.050000000003', 'Open': '44494.65', 'OpenInterest': '0', 'ScripCode': 999920005, 'SellQuantity': 0, 'TotalBuyQuantity': 0, 'TotalSellQuantity': 0, 'Volume': '0'}], 'Message': 'Success', 'Status': 0, 'TimeStamp': '/Date(1694014266670+0530)/'}
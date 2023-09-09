from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.utils.log import get_task_logger

from rsbackend.fivep.custom_5p_client import  MyStrategy, ScripMaster, DoublePlay, ExpiryDayBlitz, CustomStrategy
import os
import requests
import pandas as pd

from rsbackend.fivep.models import Fivep
import json
from py5paisa.strategy import strategies

# Cres for accessing the 5p  
cred = {
    "APP_NAME": os.getenv("P5_APP_NAME"), 
    "APP_SOURCE":os.getenv("P5_APP_SOURCE"),
    "USER_ID": os.getenv("P5_APP_USER_ID"),
    "PASSWORD": os.getenv("P5_APP_PASSWORD"),
    "USER_KEY": os.getenv("P5_APP_USER_KEY"),
    "ENCRYPTION_KEY": os.getenv("P5_APP_ENCRYPTION_KEY")
}

from datetime import datetime


# my_strat_client = None


# def setup_my_strat_client():
    
dob = os.getenv("P5_DOB")
email = os.getenv("P5_EMAIL")
password = os.getenv("P5_PASSWORD")


# fivep_user = Fivep.objects.get(id='2eba0a8d-fef9-405a-9545-f6fb6c9935d3')

# # request_token = get_access_token_from_redis()
# try:
#     # request_token = get_access_token_from_redis()
#     request_token = fivep_user.request_token

#     print("request_token", request_token)

#     my_strat_client = MyStrategy(email=email, password=password, dob=dob, cred=cred, request_token=request_token)
#     print("Completed setup_my_strat_client:")
# except Exception as e:
#     print("Error in setup_my_strat_client:", str(e))


# setup_my_strat_client()


logger = get_task_logger(__name__)


@shared_task()
def add(x,y):
    print(" Add task called and worker is running good")
    return x+y



@shared_task
def send_email(sender,to,body):
    pass


@shared_task
def sch_task_20sec():
    print("Running task ")
    
    

@shared_task
def download_scrip_master():    
    
    print(" download_scrip_master  worker is running good")
    url = 'https://images.5paisa.com/website/scripmaster-csv-format.csv'
    # url = 'https://www.facebook.com/favicon.ico'
    # r = requests.get(url, allow_redirects=True)
    # print("response is ", r)
    # open('scripmaster-csv-format.csv', 'wb').write(r.content)
    sm = ScripMaster()
    sm.download_scrip_master()

@shared_task
def daily_place_oi_change_strat_orders():
    scrip_symbol= "BANKNIFTY"
    

    # my_strat_client.get_max_risk_per_trade()
    print("Max quantity ", my_strat_client.get_quantity_per_trade(100, 25))
    # bnf_oc = my_strat_client.get_option_chain_next_week(symbol=scrip_symbol)
    pcr= my_strat_client.get_oi_change_pcr(symbol=scrip_symbol)
     # print("data type ", type(bnf_oc))
    print("oi_change is",pcr)
    
    # strategy=strategies(cred=cred,request_token=request_token)
    # strategy.short_straddle("banknifty",'37000','50','20210610','I',tag='9AMSTRAT')

    
@shared_task
def print_account_and_market_status():
    # TODO get this if token is not expired- by setting up last get time or something
    
    # fivep_user = Fivep.objects.get(id='2eba0a8d-fef9-405a-9545-f6fb6c9935d3')
    
    # # request_token = get_access_token_from_redis()
    # request_token= fivep_user.request_token
    
    # print("request_token", request_token)

    fivep_user = Fivep.objects.get(id='2eba0a8d-fef9-405a-9545-f6fb6c9935d3')
    
    # request_token = get_access_token_from_redis()
    request_token= fivep_user.request_token
    print("token is ", request_token)

    my_strat_client = MyStrategy(email=email, password=password, dob=dob, cred=cred, request_token=request_token, access_token=fivep_user.access_token, client_code=fivep_user.client_code,jwt_token=fivep_user.jwt_token)
    
    # my_strat_client.get_max_risk_per_trade()
    # print("Max quantity ", my_strat_client.get_quantity_per_trade(100, 25))
    # bnf_oc = my_strat_client.get_option_chain_next_week("NIFTY")

    # print("market status", bnf_oc)
    
    print(my_strat_client.get_market_status())

     # Print the string
    # print(dict_string)
    # bnf_oc = bnf_oc['Options']

    # bnf_oc = bnf_oc.replace("'", "\"")

    # # Parse the string as JSON
    # json_obj = json.loads(bnf_oc)

    # # Print the JSON object
    # print(json.dumps(json_obj, indent=4))
    # print("Option chain isssss",json_obj)

    # print("get_market_status",my_strat_client.get_market_status())
    # print("positions",my_strat_client.positions())
    # print("order_book, ",my_strat_client.order_book())
    # print("margin",my_strat_client.margin())



@shared_task
def task_one():
    print(" task one called and worker is running good")
    return "success"



@shared_task
def task_two(data, *args, **kwargs):
    print(f" task two called with the argument {data} and worker is running good")
    return "success"


@shared_task
def place_daily_atm_straddle_sell_with_hedge_trade():
    
    logger.info("placing the place_daily_atm_straddle_sell_with_hedge_trade ")
    symbol = "BANKNIFTY"
    
    straddle_sell_quantity = 15
    sl_hedge_quantity = 30
    
    url = 'https://images.5paisa.com/website/scripmaster-csv-format.csv'
    sm = ScripMaster()
    sm.download_scrip_master()
    logger.info("downloaded scrip")
    
    
    # Create my custom client    
    fivep_user = Fivep.objects.get(id='2eba0a8d-fef9-405a-9545-f6fb6c9935d3')
    request_token= fivep_user.request_token
    my_strat_client = MyStrategy(email=email, password=password, dob=dob, cred=cred, request_token=request_token, access_token=fivep_user.access_token, client_code=fivep_user.client_code,jwt_token=fivep_user.jwt_token)
    
    logger.info("market status is %s", my_strat_client.get_market_status())
    print("margins",my_strat_client.margin())
    print("client positions",my_strat_client.positions())
    print("client.get_tradebook()", my_strat_client.get_tradebook())
    # client.get_trade_history("PASS EXCHANGE ORDER ID")
    
    bnf_scrip = sm.get_banknifty_scrip()
    bnf_price = my_strat_client.get_cmp_for_scripcode(scripcode=bnf_scrip,exchange="N", exchange_type="C")
    straddle_price = bnf_price-bnf_price%100 # ATM price
    vix_scrip_code = sm.get_vix_scrip_code()
    daily_perc_movement = my_strat_client.get_daily_weekly_monthly_volatility(vix_scrip_code=vix_scrip_code)
    
    # logger.info("daily_movement", daily_perc_movement)
    daily_abs_movement = bnf_price*(daily_perc_movement/100)
    # logger.info("daily_abs_movement %d", daily_abs_movement-daily_abs_movement%10)
    
    daily_abs_movement_100_mul = daily_abs_movement-daily_abs_movement%10
    
    
    sl_hedge_ce_strike_price = straddle_price + daily_abs_movement_100_mul
    sl_hedge_pe_strike_price = straddle_price - daily_abs_movement_100_mul
    
    benefit_hedge_ce_strike_price = straddle_price + 2*daily_abs_movement_100_mul
    benefit_hedge_pe_strike_price = straddle_price - 2*daily_abs_movement_100_mul
    
    
    
    current_exp_timestamp,formatted_date_string = my_strat_client.get_current_exp_date(symbol=symbol)
    logger.info("formatted_date_string: %s", formatted_date_string)
    current_date = datetime.now() 
    target_date = datetime.strptime(formatted_date_string, "%Y%m%d")

    days_until_exp = (target_date - current_date).days
    print(f"Days until {formatted_date_string}: {days_until_exp} days")
    # TODO hooks days till expiry into hadge strike price selecting

    # Place CE side SL hedge trade 
    ce_option_scrip_code = sm.get_option_scripcode(underlying=symbol, option_type="CE", expriy_formated_string=formatted_date_string, strike_price=sl_hedge_ce_strike_price)
    logger.info("ce_option_scrip_code: %s", ce_option_scrip_code)
    sl_hedge_ce_price = my_strat_client.get_cmp_for_scripcode(scripcode=ce_option_scrip_code,exchange="N",exchange_type="D")
    order_details = my_strat_client.place_custom_order(OrderType="B",Exchange='N',ExchangeType='D',ScripCode=ce_option_scrip_code,Qty=sl_hedge_quantity,Price=2*sl_hedge_ce_price,IsIntraday=True,StopLossPrice=2*sl_hedge_ce_price-5)
    if order_details is None:
        return
    logger.info("order is is, ",order_details)
    
    # Place PE order  SL hedge trade 
    pe_option_scrip_code = sm.get_option_scripcode(underlying=symbol, option_type="PE", expriy_formated_string=formatted_date_string, strike_price=sl_hedge_pe_strike_price)
    sl_hedge_pe_price = my_strat_client.get_cmp_for_scripcode(scripcode=pe_option_scrip_code,exchange="N",exchange_type="D")
    
    order_details = my_strat_client.place_custom_order(OrderType="B",Exchange='N',ExchangeType='D',ScripCode=pe_option_scrip_code,Qty=sl_hedge_quantity,Price=2*sl_hedge_pe_price,IsIntraday=True,StopLossPrice=2*sl_hedge_pe_price-5)
    
    if order_details is None:
        return
    logger.info("order is is, ",order_details)
    
    # #TODO fetch order status and then only place sell trades     
    
    
    
    cs = CustomStrategy(my_strat_client=my_strat_client)
    
    
    # print("formatted_date_string", formatted_date_string)
    # #long_strangle(<symbol>,<List of sell strike price>,<qty>,<expiry>,<Order Type>)
    response = cs.long_strangle("banknifty",[straddle_price-500,straddle_price+500],straddle_sell_quantity,formatted_date_string,'I',tag='DailyStraddle')
    
    
    print("response is this", response)
    
    # #TODO fetch order status and then only place sell trades 
    
    # # my_strat_client.place_thursday_straddle_1PM_trade(symbol=symbol,cmp=bnf_price,scrip_code=bnf_scrip)
    response = cs.short_straddle("banknifty",straddle_price,straddle_sell_quantity,formatted_date_string,'I',tag='DailyStraddle')
    
    # my_strat_client.place_custom_order(OrderType="B",Exchange='N',ExchangeType='D',ScripCode=ce_option_scrip_code,Qty=15,Price=2*option_price,IsIntraday=True,StopLossPrice=2*option_price-5)
    
    # # Place PE order
    # pe_option_scrip_code = sm.get_option_scripcode(underlying=symbol, option_type="PE", expriy_formated_string=formatted_date_string, strike_price=straddle_price-300)
    # option_price = my_strat_client.get_cmp_for_scripcode(scripcode=pe_option_scrip_code,exchange="N",exchange_type="D")
    
    # my_strat_client.place_custom_order(OrderType="B",Exchange='N',ExchangeType='D',ScripCode=pe_option_scrip_code,Qty=15,Price=2*option_price,IsIntraday=True,StopLossPrice=2*option_price-5)
    
    
    # #TODO fetch order status and then only place sell trades     
    
    # print("formatted_date_string", formatted_date_string)
    # #long_strangle(<symbol>,<List of sell strike price>,<qty>,<expiry>,<Order Type>)
    # response = my_strat_client.strategy.long_strangle("banknifty",[straddle_price-500,straddle_price+500],15,formatted_date_string,'I',tag='DailyStraddle')
    
    # #TODO fetch order status and then only place sell trades 
    
    # # my_strat_client.place_thursday_straddle_1PM_trade(symbol=symbol,cmp=bnf_price,scrip_code=bnf_scrip)
    # response = my_strat_client.strategy.short_straddle("banknifty",straddle_price,15,formatted_date_string,'I',tag='DailyStraddle')
    
    # strategy.squareoff('tag')
    
    
@shared_task
def exit_place_daily_atm_straddle_sell_with_hedge_trade():
    # Create my custom client    
    fivep_user = Fivep.objects.get(id='2eba0a8d-fef9-405a-9545-f6fb6c9935d3')
    request_token= fivep_user.request_token
    my_strat_client = MyStrategy(email=email, password=password, dob=dob, cred=cred, request_token=request_token, access_token=fivep_user.access_token, client_code=fivep_user.client_code,jwt_token=fivep_user.jwt_token)
    
    my_strat_client.squareoff_all()
    print("Square offed all")
   
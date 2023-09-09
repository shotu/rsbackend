
"""sumary_line"""

import logging
import os
from time import sleep


logger = logging.getLogger(__name__)

from celery import shared_task
from celery.contrib.abortable import AbortableTask
from dotenv import load_dotenv
from redis import Redis

load_dotenv()

# Check if we're running inside Docker Compose
if 'DOCKER_COMPOSE' in os.environ:
    # If we're inside Docker Compose, use the service name as the Redis host
    REDIS_HOST = os.environ['REDIS_HOST']
else:
    # If we're outside Docker Compose, use localhost as the Redis host
    REDIS_HOST = 'localhost'

# Create a Redis instance using the configured host and port
redis = Redis(host=REDIS_HOST, port=6379)

from .my_strategy import MyStrategy
from .scrip_master import ScripMaster

logger = logging.getLogger(__name__)

import math

from py5paisa.order import Exchange, Order, OrderType

from .helper import get_access_token_from_redis

# Note: This is an indicative order.


#You can pass scripdata either you can pass scripcode also.
# please use price = 0 for market Order
#use IsIntraday= true for intraday orders

# Cres for accessing the 5p  

cred = {
    "APP_NAME": os.getenv("P5_APP_NAME"), 
    "APP_SOURCE":os.getenv("P5_APP_SOURCE"),
    "USER_ID": os.getenv("P5_APP_USER_ID"),
    "PASSWORD": os.getenv("P5_APP_PASSWORD"),
    "USER_KEY": os.getenv("P5_APP_USER_KEY"),
    "ENCRYPTION_KEY": os.getenv("P5_APP_ENCRYPTION_KEY")
}


dob = os.getenv("P5_DOB")
email = os.getenv("P5_EMAIL")
password = os.getenv("P5_PASSWORD")


class DoublePlay(MyStrategy):

    def __init__(self) -> None:
        request_token = get_access_token_from_redis()
        # self = MyStrategy(email=email, password=password, dob=dob, cred=cred, request_token=request_token)
        super().__init__(email= email, password=password, dob=dob, cred=cred, request_token=request_token)
        
    def place_entry_orders(self):
        
        are_exchanges_open = self.are_both_currency_and_derivative_exchange_open()
        if not are_exchanges_open:
            logger.info("Both currency and dervatives exchanges are not open. Not placing order")
            return
        
        sm = ScripMaster()
        max_risk_per_leg = self.get_max_risk_per_trade()
        logger.info("max_risk_per_leg", max_risk_per_leg)
        nifty_fut_curent_price = self.get_last_traded_price(exch="N",exch_type="C",  symbol="NIFTY")
        current_fut_price = nifty_fut_curent_price
        nifty_option_type = "CE"
        range_size = 50
        root = "NIFTY"
        nifty_lot_size = 50   
        # Get nifty next expiry ce script
        next_expiry_ce_scrip_nifty = sm.get_next_week_or_monthly_future_scrip_details(exch="N", exch_type = "D", root = root, option_type=nifty_option_type, current_fut_price= current_fut_price, range_size= range_size)
        # Get ce price
        nifty_atm_ce_price= self.get_last_traded_price(exch=next_expiry_ce_scrip_nifty["Exch"], exch_type=next_expiry_ce_scrip_nifty["ExchType"], symbol=next_expiry_ce_scrip_nifty["Name"])
        
        max_lot_buy = math.floor(max_risk_per_leg/(nifty_atm_ce_price*nifty_lot_size))
        logger.info("Max lot", max_lot_buy)
        
        nifty_deployed_capital = max_lot_buy*nifty_lot_size*nifty_atm_ce_price
        logger.info("next_expiry_ce_scrip_nifty", next_expiry_ce_scrip_nifty)
        
         # For USDINR
        # First get the fut price script of usdinr for next week
        usdinr_fut_price_next_week_scrip = sm.get_next_exp_fut_scrip_details(exch="N", exch_type="U",root="USDINR",cp_type="XX"  )
        # Get fture porice
        usdinr_fut_curent_price = self.get_last_traded_price(exch="N",exch_type="U",  symbol=usdinr_fut_price_next_week_scrip["Name"])
        logger.info("usdinr_fut_curent_price", usdinr_fut_curent_price)
        usdinr_range = 0.25
        # Get CE script
        next_expiry_ce_scrip_usdinr = sm.get_next_week_or_monthly_future_scrip_details(exch= "N",exch_type = "U", root = "USDINR", option_type="CE", current_fut_price= usdinr_fut_curent_price, range_size= usdinr_range)
        # Get atm ce price
        usdinr_atm_ce_price= self.get_last_traded_price(exch=next_expiry_ce_scrip_usdinr["Exch"], exch_type=next_expiry_ce_scrip_usdinr["ExchType"], symbol=next_expiry_ce_scrip_usdinr["Name"])
        
        # Max quantity wert nifty deployted capital
        usdinr_quantity= nifty_deployed_capital/(usdinr_atm_ce_price*1000)
        # usdinr_quantity = 2       
        # Place usdinr order at CMRP
        try:
            response = self.place_custom_order(scrip_details=next_expiry_ce_scrip_usdinr, quantity=usdinr_quantity, price=0)
            logger.info(response)
        except Exception as e:
            logger.error("Error placing order usdinr", e)

        # Then place nifty after, as chances are high for failing of USDINR order
        try:
            result= self.place_custom_order(scrip_details=next_expiry_ce_scrip_nifty, quantity=max_lot_buy*50, price=0)
        except Exception as e:
            logger.error("Error placing the order nifty", e)
        finally:
            # TODO Here send the message or email for success or failure, with current postions
            pass

    # Places ther custom order for scrip details
    # For ATM orders pass price= 0         
    def place_custom_order(self, scrip_details, quantity, price):
        logger.info("Placing order for - scrip", scrip_details)
        return self.place_order(OrderType="B",Exchange="N", ExchangeType=scrip_details["ExchType"], ScripCode = int(scrip_details["Scripcode"]), Qty=quantity, Price=price)

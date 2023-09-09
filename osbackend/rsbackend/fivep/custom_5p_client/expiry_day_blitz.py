
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


class ExpiryDayBlitz(MyStrategy):

    def __init__(self) -> None:
        request_token = get_access_token_from_redis()
        # self = MyStrategy(email=email, password=password, dob=dob, cred=cred, request_token=request_token)
        super().__init__(email= email, password=password, dob=dob, cred=cred, request_token=request_token)
        
    def place_entry_orders(self):
        symbol="BANKNIFTY"
        sm = ScripMaster()
        current_fut_price = self.get_cmp_for_symbol(symbol)
        
        # strike_price_ce = round((current_fut_price) / 100)   # TODO Balance this in terms of price differences
        # strike_price_pe = round((current_fut_price) / 100) 
        # expiry_date = self.get_current_exp_date(symbol)
        
        range_size = 100
        root = "BANKNIFTY"
        banknifty_lot_size = 25 #TODO Keep check on this l;ot size for Nifty Bank futures and options to 15 from 25. The new rule is applicable from the beginning of July 2023 contracts

        
        banknifty_option_type = "CE"
        # Get nifty next expiry ce script
        next_expiry_ce_scrip_banknifty = sm.get_next_week_or_monthly_future_scrip_details(exch="N", exch_type = "D", root = root, option_type=banknifty_option_type, current_fut_price= current_fut_price, range_size= range_size)
        # Get ce price
        banknifty_atm_ce_price= self.get_last_traded_price(exch=next_expiry_ce_scrip_banknifty["Exch"], exch_type=next_expiry_ce_scrip_banknifty["ExchType"], symbol=next_expiry_ce_scrip_banknifty["Name"])
        

        logger.info("banknifty_atm_ce_price", banknifty_atm_ce_price)

        banknifty_option_type = "PE"
        # Get nifty next expiry ce script
        next_expiry_pe_scrip_banknifty = sm.get_next_week_or_monthly_future_scrip_details(exch="N", exch_type = "D", root = root, option_type=banknifty_option_type, current_fut_price= current_fut_price, range_size= range_size)
        # Get ce price
        banknifty_atm_pe_price= self.get_last_traded_price(exch=next_expiry_pe_scrip_banknifty["Exch"], exch_type=next_expiry_pe_scrip_banknifty["ExchType"], symbol=next_expiry_pe_scrip_banknifty["Name"])
        

        logger.info("banknifty_atm_pe_price", banknifty_atm_pe_price)

        max_lot_buy =1 
        # Then place nifty after, as chances are high for failing of USDINR order
        try:
            result= self.place_custom_order(scrip_details=next_expiry_pe_scrip_banknifty, quantity=max_lot_buy*banknifty_lot_size, price=0)
        except Exception as e:
            logger.error("Error placing the order banknifty pe", e)
        finally:
            # TODO Here send the message or email for success or failure, with current postions
            pass
        

        logger.info("banknifty_atm_ce_price", banknifty_atm_pe_price)

        # Then place nifty after, as chances are high for failing of USDINR order
        try:
            result= self.place_custom_order(scrip_details=next_expiry_ce_scrip_banknifty, quantity=max_lot_buy*banknifty_lot_size, price=0)
        except Exception as e:
            logger.error("Error placing the order banknifty ce", e)
        finally:
            # TODO Here send the message or email for success or failure, with current postions
            pass

    def place_custom_order(self, scrip_details, quantity, price):
        logger.info("scrip_details", scrip_details)
        return self.place_order(OrderType="B",Exchange="N", ExchangeType=scrip_details["ExchType"], ScripCode = int(scrip_details["Scripcode"]), Qty=quantity, Price=price)


    # Exit the db orders
    def exit_all_orders(self):
        #TODO change this to exit only orders wrt to entry oreders- as it will exit all other orders too
        try:
            self.squareoff_all()
            logger.info("Order exiting is success")
        except Exception as e:
            logger.error("Error squaring off all orders")
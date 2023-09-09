
#Import strategy package
import logging
logger = logging.getLogger(__name__)
from .custom_data_client import CustomDataClient
from datetime import datetime
import math
#Import strategy package
from py5paisa.strategy import *
from py5paisa.order import Order, OrderType, Exchange
class MyStrategy(CustomDataClient): 
    # email, password, dob, cred, request_token, 
    
    def __init__(self, email, password, dob, cred, request_token, access_token= None, jwt_token= None, client_code = None):
        super().__init__(email=email, password=password, dob=dob, cred=cred, request_token=request_token)
        # user=None, passw=None, dob=None, cred=None, request_token=None
        self.request_token = request_token
        # self.get_oauth_session(request_token)
        
        if access_token == None:
            access_token = self.get_access_token(request_token)

        else:
             
            self.access_token = access_token
            self.Jwt_token= jwt_token
            self.client_code = client_code
            
        print("access token isssss",access_token)
       
        
        # self.strategy = strategies(cred=cred,request_token=request_token)

        # self.data_client = CustomDataClient(email, password, dob, cred, request_token)


    def get_cmp_for_scripcode(self, scripcode, exchange, exchange_type):
        print("scrip_code is",scripcode)
        price = self.fetch_market_depth_by_scripcode(Exchange=exchange,ExchangeType=exchange_type,ScripCode=scripcode)

        print("price is", price)
        
        
        return price

    def place_custom_order(self,OrderType,Exchange,ExchangeType, ScripCode, Qty, Price,IsIntraday,StopLossPrice):
        # refer https://www.5paisa.com/developerapi/order-request-place-order
        order_result= self.place_order(OrderType=OrderType,Exchange=Exchange,ExchangeType=ExchangeType, ScripCode = str(ScripCode), Qty=Qty, Price=Price,IsIntraday=IsIntraday, StopLossPrice=StopLossPrice)
        print("order_result",order_result)
        return order_result
    
    def get_max_risk_per_trade(self):

        max_risk_divider = 8
        margin = self.margin()
        available_margin = margin[0]['AvailableMargin']
        print("AvailableMargin, is", available_margin)
        max_risk = available_margin/max_risk_divider
        print(" max risk per trade is , ", max_risk)
        return max_risk
    
    def get_quantity_per_trade(self, cmp, lot_size):
        
        max_risk_per_trade = self.get_max_risk_per_trade()
        print("max riks per trade is ssssss", max_risk_per_trade)

        one_lot_amount = cmp*lot_size

        max_lot_can_buy = math.floor(max_risk_per_trade/one_lot_amount)
        return max_lot_can_buy*lot_size


     # Symbvol should be NIFTY/BANKNIFTY
    def get_scrip_code_and_cmp_string_for_option(self,symbol, expiry_date, option_type, strike_price):
        # expiry_date = '20230413'
        
        date_obj = datetime.strptime(expiry_date, '%Y%m%d')  # parse date string to datetime object
        formatted_date_str = date_obj.strftime('%d %b %Y')  # format datetime object to desired string format
        
        print(formatted_date_str)  # output: '13 Apr 2023'
        req_symbol= symbol.upper() + " " + formatted_date_str.upper() + " " +option_type.upper() + " " + str(strike_price)+".00"
        
        print("req_symbol", req_symbol)
        print("strike price is ", strike_price)
        print("expiry_date",expiry_date)
        # req_list_=[{"Exch":"N","ExchType":"D","Symbol":"NIFTY 22 APR 2021 CE 15200.00","Expiry":"20210422","StrikePrice":"15200","OptionType":"CE"}]

        req_list_=[{"Exch":"N","ExchType":"D","Symbol": req_symbol,"Expiry": expiry_date,"StrikePrice":strike_price,"OptionType":option_type.upper()}]
        
        feed = self.fetch_market_feed(req_list_)

        token = feed['Data'][0]['Token']
        print("feed is", feed)
        cmp = feed['Data'][0]['LastRate']
        # return token, 
        print("scrip_code", token)

        print("cmp", cmp)
        return token, cmp
    
    def place_thursday_straddle_1PM_trade(self, symbol, cmp, scrip_code):

        print("cmp of bnf", cmp)
        symbol="BANKNIFTY"
        strike_price_ce = round((cmp) / 100)   # TODO Balance this in terms of price differences
        strike_price_pe = round((cmp) / 100) 
        expiry_date,formatted_date_string = self.get_current_exp_date(symbol)
        
        ce_scrip_code,ce_cmp = self.get_scrip_code_and_cmp_string_for_option(symbol="BANKNIFTY",expiry_date=formatted_date_string,option_type="CE",strike_price=strike_price_ce)
        pe_scrip_code,pe_cmp = self.get_scrip_code_and_cmp_string_for_option(symbol="BANKNIFTY",expiry_date=formatted_date_string,option_type="PE",strike_price=strike_price_pe)

        quantity = self.get_quantity_per_trade(ce_cmp, 15) #TODO get lot size programmatically  The National Stock Exchange has reduced the market 
        #lot size for Nifty Bank futures and options to 15 from 25. The new rule is applicable from the beginning of July 2023 contracts
        # place market order
        order_res = self.place_order(OrderType='B',Exchange='N',ExchangeType='D', ScripCode = ce_scrip_code, Qty=quantity, Price=0, StopLossPrice=5, IsIntraday=True)
        print("order_Res ce", order_res)
        if order_res['Message'].upper()!="SUCCESS":
            logger.debug("Order placing failed", order_res)
        order_res = self.place_order(OrderType='B',Exchange='N',ExchangeType='D', ScripCode = pe_scrip_code, Qty=quantity, Price=0, StopLossPrice=5, IsIntraday=True)
        
        print("order_Res pe", order_res)
        if order_res['Message'].upper()!="SUCCESS":
            logger.debug("Order placing failed", order_res)
        print("order_res 2", order_res)
    
    # used for exiting straddle placed on thursday
    def place_exit_all_orders_thursday(self):
        self.squareoff_all()
        print("Exited all order on Thursday")

    # Check if both the excahnges- NSE currency and derivatoive are open
    def are_both_currency_and_derivative_exchange_open(self):
        data = self.get_market_status()
        
        derivative_open = any(exchange['Exch'] == 'N' and exchange['ExchType'] == 'D' and exchange['MarketStatus'] == 'Open' for exchange in data)
        currency_open = any(exchange['Exch'] == 'N' and exchange['ExchType'] == 'U' and exchange['MarketStatus'] == 'Open' for exchange in data)

        return derivative_open and currency_open
    
    # def 
    
    #     # Executes the current week OTM strangle  BANKNIFTY- mainly meant for hedging straddle
    # def current_week_long_strangle_bnf(self):
    #     symbol = "BANKNIFTY"
    #     cmp = self.get_cmp_for_symbol(symbol)
    #     current_vix = 18 # TODO get this realtime 
    #     range_value = 700
    #     rounded_value_down = round((cmp - range_value) / 100) * 100
    #     logging.info("rounded_value_down", rounded_value_down)
    #     rounded_value_up = round((cmp + range_value) / 100) * 100
    #     logging.info("rounded_value_up", rounded_value_up)
    #     quantitiy = 25 # lots*25
    #     expiry_date = self.data_client.get_current_exp_date(symbol)
        
    #     logging.info("Execuring the long straddle BANKNIFTY ")
    #     # exchange_order_ids = self.strategy.long_strangle("banknifty",[rounded_value_down,rounded_value_up ],quantitiy,expiry_date,'D')
        
    #     #long_straddle(<symbol>,<strike price>,<qty>,<expiry>,<Order Type>)
    #     # self.strategy.long_straddle("banknifty",'41000','25','20230413','I',tag='Test')
    #     #long_strangle(<symbol>,<List of sell strike price>,<qty>,<expiry>,<Order Type>)
    #     self.long_strangle("banknifty",[rounded_value_down,rounded_value_up],quantitiy,expiry_date,'I',tag='BANKNIFTY_STRANGLE')

    #     #Using tag is optional
    #     # TODO SAVE THESE IDS TO REDIS FOR EXIT STRATEGIES
    #     # print("exchange_order_ids",exchange_order_ids)


    # Executes short straddle BANKNIFTY at ATM of current week
    # def current_week_short_straddle_bnf(self):
    #     symbol = "BANKNIFTY"
    #     cmp = self.get_cmp_for_symbol(symbol)
    #     #short_straddle(<symbol>,<strike price>,<qty>,<expiry>,<Order Type>) 
    #     rounded_value_atm = round((cmp) / 100) * 100
    #     logging.info("rounded_value_atm: ", rounded_value_atm)
    #     quantity = 25 #TODO get lot size programmatically  The National Stock Exchange has reduced the market lot size for Nifty Bank futures and options to 15 from 25. The new rule is applicable from the beginning of July 2023 contracts
    #     expiry_date = self.get_current_exp_date(symbol)
    #     logging.info("Execuring the short straddle BANKNIFTY ")
    #     self.strategy.short_straddle("banknifty", rounded_value_atm, quantity, expiry_date,'I',tag='BANKNIFTY_SHORT_STRADDLE')

    #     # self.strategy.short_straddle#short_straddle(<symbol>,<strike price>,<qty>,<expiry>,<Order Type>)
    #     # self.strategy.short_straddle("banknifty",'41000','25','20230413','I',tag='SOME_NAME')

    # Executes the current week OTM strangle  NIFTY- mainly meant for hedging straddle
    # def current_week_long_strangle_nifty(self):
    #     symbol = "NIFTY"
    #     cmp = self.get_cmp_for_symbol(symbol)
    #     current_vix = 18 # TODO get this realtime 
    #     range_value = 500
    #     rounded_value_down = round((cmp - range_value) / 100) * 100
    #     rounded_value_up = round((cmp + range_value) / 100) * 100
    #     quantitiy = 50 # lots*25 # Calculate this real time 
    #     expiry_date = self.data_client.get_current_exp_date(symbol)
    #     logging.info("Execuring the long straddle NIFTY ")
    #     self.strategy.long_strangle("nifty",[rounded_value_down, rounded_value_up],quantitiy,expiry_date,'D')

#Using tag is optional
    # Executes short straddle NIFTY at ATM of current week 
    # def current_week_short_straddle_nifty(self):
    #     symbol = "NIFTY"
    #     cmp = self.get_cmp_for_symbol(symbol)
    #     #short_straddle(<symbol>,<strike price>,<qty>,<expiry>,<Order Type>) 
    #     rounded_value_atm = round((cmp) / 100) * 100
    #     quantity = 40 #TODO get lot size programmatically  The National Stock Exchange has reduced the market lot size for Nifty Bank futures and options to 15 from 25. The new rule is applicable from the beginning of July 2023 contracts
    #     expiry_date = self.data_client.get_current_exp_date(symbol)
    #     logging.info("Execuring the short straddle NIFTY with expiry_date", expiry_date)
    #     self.strategy.short_straddle("nifty", rounded_value_atm, quantity, expiry_date,'I',tag='NIFTY_SHORT_STRADDLE')

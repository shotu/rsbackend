from py5paisa import FivePaisaClient
#Import strategy package
from py5paisa.strategy import strategies
from datetime import timedelta, datetime, date

from redis import Redis
import time
redis = Redis(host="redis", port=6379)
import requests
import pandas as pd
import json
import math

class CustomDataClient(FivePaisaClient ):
  
    def __init__(self, email, password, dob, cred, request_token, ):
        super().__init__(cred=cred)
        
        self.request_token = request_token
        print("coming here ")
        # self.get_oauth_session(request_token)
    
    def get_market_status(self):
        market_status = super().get_market_status()
        print("market status:", market_status[0])
        
    def get_all_positions(self):
        return self.positions()
    
    def get_daily_weekly_monthly_volatility(self, vix_scrip_code ):
        
        vix_price = self.fetch_market_depth_by_scripcode(ScripCode=vix_scrip_code,Exchange="N", ExchangeType="D")
        
        print("vix_price", vix_price)
        annual_volatility = vix_price
        trading_days_per_year = 252

        daily_volatility_precise = annual_volatility / math.sqrt(trading_days_per_year)
        daily_volatility_rule_of_16 = annual_volatility / 16
        print(f"Annual Volatility: {annual_volatility}%")
        print(f"Daily Volatility (Precise): {daily_volatility_precise:.2f}%")
        print(f"Daily Volatility (Rule of 16): {daily_volatility_rule_of_16:.2f}%")

        return daily_volatility_rule_of_16
        
    
    
    def fetch_market_depth_by_scripcode(self, Exchange,ExchangeType,ScripCode):
        # makret_depth = super().fetch_market_depth_by_scrip(Exchange= Exchange,ExchangeType =ExchangeType,ScripCode=ScripCode)
        # print("market depth", makret_depth)
        
        a=[{"Exchange":Exchange,"ExchangeType":ExchangeType,"ScripCode":str(ScripCode)},]
  
        # print("full walai", self.fetch_market_depth(a))
        market_depth = self.fetch_market_depth(a)
        
        
        
        return market_depth['Data'][0]['LastTradedPrice']
        
    # def fetch_market_depth_by_symbol(self, symbol_list):
    #     return self.fetch_market_depth_by_symbol(symbol_list)

    def get_last_traded_price(self, symbol, exch, exch_type):
        
      
        symbol_list = [{"Exchange":exch,"ExchangeType": exch_type,"Symbol":symbol}]
                            # BANKNIFTY 31 Feb 2022 CE 41600.00
        market_depth = self.fetch_market_depth_by_symbol(symbol_list)
        # print(client.fetch_market_depth(a))
        
        print("market_depth", market_depth)

        return market_depth['Data'][0]['LastTradedPrice']

    def get_price_by_scriup_code(self,exch, exch_type, scrip_code ):
        a=[{"Exchange":exch,"ExchangeType":exch_type,"ScripCode": int(scrip_code)},]
        
        print("a is",a  )
        market_depth =self.fetch_market_depth(a)
        
        print("market_depth", market_depth)

        # return market_depth['Data'][0]['LastTradedPrice']
        # self.fetch_market_depth(scripcode="12345")

    def get_market_feed(self, req_list ):
        # req_list= [{"Exch":exch, "ExchType": exch_type, "Symbol": symbol, "Expiry": expiry, "StrikePrice": strike_price, "OptionType": option_type}]
        # req_list_=[{"Exch":"N","ExchType":"D","Symbol":"NIFTY 22 APR 2021 CE 15200.00","Expiry":"20210422","StrikePrice":"15200","OptionType":"CE"},]
            # {"Exch":"N","ExchType":"D","Symbol":"NIFTY 22 APR 2021 PE 15200.00","Expiry":"20210422","StrikePrice":"15200","OptionType":"PE"}]
        self.fetch_market_feed(req_list)

    def get_option_chain_next_week(self, symbol):
        
        next_week_exp_date, formatted_exp_date = self.get_current_exp_date(symbol=symbol)
        
        print("Next week exp date", next_week_exp_date)
        
        option_chain = self.get_option_chain("N",symbol,next_week_exp_date)
        
        
        # Get today's date
        # now = datetime.now()

        # # Calculate days until next Thursday
        # days_until_thursday = (3 - now.weekday()) % 7 -1 

        # # Find date and time of next Thursday at 14:30
        # next_thursday = now + timedelta(days=days_until_thursday)
        

        # next_thursday = next_thursday.replace(hour=14, minute=30, second=0, microsecond=0)
        # timestamp = int(next_thursday.timestamp())

        # print("next_thursday",next_thursday)
        # # Convert to timestamp in milliseconds
        # timestamp = int(timestamp*1000)

        # print("Timestamp in milliseconds for next Thursday:", timestamp)

        # print("timestamp Type is ", type(timestamp))

        # # client.get_option_chain("N","NIFTY",<Pass expiry timestamp from get_expiry response>)
        # try:
            
        #     option_chain = self.get_option_chain_next_week(symbol=symbol)
        #     return option_chain
        # except Exception as e:
        #     print("Exception is",e)
        #     return e
        # print("option_chain",option_chain)
        return option_chain 
    
    def get_oi_change_pcr(self,symbol):
        oi_chain = self.get_option_chain_next_week(symbol=symbol)
        # logger.debug("oc is ", bnf_oc['Options'])
        df = pd.DataFrame(oi_chain['Options'])
        # print(df[0])
        # print(df.iloc[0])

        # Convert the dictionary to a string
        dict_string = json.dumps(oi_chain['Options'])

        sum_pe = 0
        sum_ce = 0

        for d in oi_chain['Options']:
            if d["CPType"] == "PE":
                sum_pe += d["ChangeInOI"]
            elif d["CPType"] == "CE":
                sum_ce += d["ChangeInOI"]

        print("Sum of ChangeInOI for PE: ", sum_pe)
        print("Sum of ChangeInOI for CE: ", sum_ce)
        oi_change_pcr = sum_pe/sum_ce
        print("oi_change_pcr",oi_change_pcr)
        
        return oi_change_pcr

    def get_sorted_active_expiries(self, symbol):
        nifty_expiries = self.get_expiry("N",symbol)
        expiry_dates = nifty_expiries['Expiry']
        sorted_expiry_dates = sorted(expiry_dates, key=lambda d: int(d['ExpiryDate'][6:-7]))
        print("sorted_expiry_dates of first ", sorted_expiry_dates[0]["ExpiryDate"][6:19]) # way to get only the timestamp
        return sorted_expiry_dates
    
    def get_current_exp_date(self, symbol):
        current_exp_timestamp = int(self.get_sorted_active_expiries(symbol=symbol)[0]["ExpiryDate"][6:19])
        # Convert timestamp to datetime object
        dt_obj = datetime.fromtimestamp(current_exp_timestamp/1000)

        # Format datetime object to desired date string format 20210626
        formatted_date_string = dt_obj.strftime('%Y%m%d')

        print(formatted_date_string)
        return current_exp_timestamp,formatted_date_string

    def analyse_option_chain(self, symbol):
        #TODO calculate PCR, relative pcr, pcr trend, OI change, PCR,  Max Pain, etc. max OI
        pass
    
    def get_cmp_for_symbol(self, symbol):
        symbol_list = [{"Exchange":"N","ExchangeType":"C","Symbol":symbol}]
        market_depth = self.fetch_market_depth_by_symbol(symbol_list)
        return market_depth['Data'][0]['LastTradedPrice']
    

    def get_cmp_for_usdinr_symbol(self, symbol):
        symbol_list = [{"Exchange":"N","ExchangeType":"U","Symbol":symbol}]
        market_depth = self.fetch_market_depth_by_symbol(symbol_list)
        return market_depth['Data'][0]['LastTradedPrice']
    

    def get_current_trades(self):
        # To get list of current trades use:-
        print(self.get_trade())


    def get_positions(self):
        positions = self.positions()
        print("Positions are: ", positions)


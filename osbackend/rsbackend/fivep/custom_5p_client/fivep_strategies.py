#Import strategy package
from py5paisa.strategy import *


from rsbackend.fivep.models import Fivep
import json
from py5paisa.strategy import strategies
import os
# Cres for accessing the 5p  
# cred = {
#     "APP_NAME": os.getenv("P5_APP_NAME"), 
#     "APP_SOURCE":os.getenv("P5_APP_SOURCE"),
#     "USER_ID": os.getenv("P5_APP_USER_ID"),
#     "PASSWORD": os.getenv("P5_APP_PASSWORD"),
#     "USER_KEY": os.getenv("P5_APP_USER_KEY"),
#     "ENCRYPTION_KEY": os.getenv("P5_APP_ENCRYPTION_KEY")
# }
from rsbackend.fivep.custom_5p_client import  MyStrategy, ScripMaster, DoublePlay, ExpiryDayBlitz
from datetime import datetime


# my_strat_client = None


# def setup_my_strat_client():
    
# dob = os.getenv("P5_DOB")
# email = os.getenv("P5_EMAIL")
# password = os.getenv("P5_PASSWORD")


# # Create my custom client    
# fivep_user = Fivep.objects.get(id='2eba0a8d-fef9-405a-9545-f6fb6c9935d3')
# request_token= fivep_user.request_token

# my_strat_client = MyStrategy(email=email, password=password, dob=dob, cred=cred, request_token=request_token, access_token=fivep_user.access_token, client_code=fivep_user.client_code,jwt_token=fivep_user.jwt_token)


# strategy=strategies(cred=cred,request_token=request_token)



class CustomStrategy(strategies):
    
    def __init__(self, my_strat_client):
        # Call the parent class's __init__ method
        # super().__init__(arg1, arg2)

        # Perform additional initialization for the child class
        self.Client = my_strat_client

    # Child class-specific method
    # def child_method(self):
    #     print("child method")
    #     pass

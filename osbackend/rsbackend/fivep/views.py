from django.shortcuts import render

# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.response import Response
from django.http import Http404
from uuid import UUID
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Fivep
from .serializers import FivepSerializer, FivepCallbackSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.filters import SearchFilter

from rest_framework import viewsets

from rest_framework import filters
# from django_filters.rest_framework import DjangoFilterBackend
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rsbackend.fivep.custom_5p_client import  MyStrategy, ScripMaster, DoublePlay, ExpiryDayBlitz
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



my_strat_client = None






# from django_filters import rest_framework as filters
# Create your views here.
# @api_view(['GET'])
# def getFiveptoken(request):
#     food = Fivep.objects.all()
#     serializer = FivepSerializer(food, many=True)
#     return Response(serializer.data)


# @api_view(['POST'])
# def postFiveptoken(request):
#     serializer = FivepSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)



class FivepListAPIView(ListCreateAPIView):
    serializer_class = FivepSerializer

    queryset = Fivep.objects.all()

    # permission_classes = [permissions.IsAuthenticated, IsOwner]

    
    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        return self.queryset.filter()
    
    # def perform_update(self, serializer):
    #     instance = self.get_object()  # instance before update
    #     # self.request.data.get("title", None)  # read data from request
        
    #     if self.request.user.is_authenticated:
    #         updated_instance = serializer.save(author=self.request.user)
    #     else:
    #         updated_instance = serializer.save()
    #     return updated_instance

class FivepDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = FivepSerializer
    queryset = Fivep.objects.all()
    lookup_field = 'id'  # Specify the lookup field to be used for retrieving the instance
    partial = True  # Allow partial updates

    def perform_update(self, serializer):
        # print(serializer.errors)  # Debugging

        serializer.save()
    
    


# callback apis for recieving request token
#https://f2bf-171-76-87-249.ngrok-free.app/?RequestToken=eyJhbGciOipXVCJ9.eyJm9sZSI6IkJtNVE2Q3J0UWtHQ2VvbFJDTW94MGlqVktyZWdyMHUxIiwiU3RhdGUiOiIiLCJuYmYiOjE2OTM2MzU5MjgsImV4cCI6MTY5MzYzNTk4OCwiaWF0IjoxNjkzNjM1OTI4fQ.rotvrBATSiGPlBaZhM0VO3h4VfPlNp3ye61sA50FcHk&state=
class CustomAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='RequestToken',  # Query parameter name
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='The request token',
            ),
        ],
        operation_description='Your API operation description here.',
        responses={200: 'OK'},
    )
    
    def get(self, request, id):
        print(id)
        # queryset = Fivep.objects.all()
        # serializer_class = FivepSerializer
        # lookup_field = 'id'
        
        # # Retrieve the 'RequestToken' query parameter from the URL
        request_token = request.query_params.get('RequestToken')
        
        
        # def setup_my_strat_client():
            
        dob = os.getenv("P5_DOB")
        email = os.getenv("P5_EMAIL")
        password = os.getenv("P5_PASSWORD")


        fivep_user = Fivep.objects.get(id='2eba0a8d-fef9-405a-9545-f6fb6c9935d3')

        # request_token = get_access_token_from_redis()
        try:
            # request_token = get_access_token_from_redis()
            # request_token = fivep_user.request_token

            print("request_token", request_token)

            my_strat_client = MyStrategy(email=email, password=password, dob=dob, cred=cred, request_token=request_token)
            print("Completed setup_my_strat_client:")
        except Exception as e:
            print("Error in setup_my_strat_client:", str(e))

        print("my start client",my_strat_client)
        print("my_strat_client.access_token",my_strat_client.access_token)
        access_token = my_strat_client.access_token
        print("my_strat_client.request_token",my_strat_client.request_token)
        print("my_strat_client.client_code",my_strat_client.client_code)
        client_code = my_strat_client.client_code
        jwt_token = my_strat_client.Jwt_token
        
        print("my_strat_client.Jwt_token",my_strat_client.Jwt_token)
        
            # my_strat_client.client_code = ""
            # my_strat_client.Jwt_token = ""
            # my_strat_client.Aspx_auth = None
            # my_strat_client.web_url = None
            # my_strat_client.market_depth_url = None
            # my_strat_client.Res_Data = None
            # my_strat_client.ws = None
            # my_strat_client.access_token = ""
            # my_strat_client.request_token = None
            # my_strat_client.session = requests.Session()
            # my_strat_client.APP_SOURCE = cred["APP_SOURCE"]
            # my_strat_client.APP_NAME = cred["APP_NAME"]
            # my_strat_client.USER_ID = cred["USER_ID"]
            # my_strat_client.PASSWORD = cred["PASSWORD"]
            # my_strat_client.USER_KEY = cred["USER_KEY"]
            # my_strat_client.ENCRYPTION_KEY = cred["ENCRYPTION_KEY"]
            # self.payload["head"]["Key"] = self.USER_KEY
            # self.payload["body"]["RequestToken"] = request_token
            # self.payload["body"]["EncryKey"] = self.ENCRYPTION_KEY
            # self.payload["body"]["UserId"] = self.USER_ID
            # url = ACCESS_TOKEN_ROUTE

            # res = self.session.post(url, json=self.payload).json()
            # message = res["body"]["Message"]

            # if message == "Success":
            #     self.access_token = res["body"]["AccessToken"]
            #     self.Jwt_token = self.access_token
            #     self._set_client_code(res["body"]["ClientCode"])
            #     log_response("Logged in!!")
            #     return self.access_token
            # else:
        
        
        Fivep.objects.filter(id=id).update(request_token=request_token,access_token=access_token,client_code = client_code, jwt_token=jwt_token)
        
        # Your API logic here...
        
        return Response({'RequestToken': request_token, 'id': id})
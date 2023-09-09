from py5paisa import FivePaisaClient
#Import strategy package
from py5paisa.strategy import strategies
from datetime import timedelta, datetime, date

from redis import Redis
import time
redis = Redis(host="redis", port=6379)
import requests

def get_access_token_from_redis():

    # Get the saved token and timestamp from Redis, if it exists
    request_token = redis.get('request_token')
    saved_timestamp = redis.get('timestamp')

    # Check if the saved timestamp is more than 4 hours ago
    
    if request_token and saved_timestamp is not None and time.time() - float(saved_timestamp) < 4 * 60 * 60:
        # Use the saved token
        request_token = request_token.decode('utf-8')  # Decode the binary value from Redis
    else:
        # Make a new request for a token
        response = requests.get('http://sel-api.dev:3000/setup-token')
        token = response.text
        print("token is", token)
        request_token = token
        # Save the new token and timestamp to Redis
        redis.set('request_token', token)
        redis.set('timestamp', time.time())

    return request_token

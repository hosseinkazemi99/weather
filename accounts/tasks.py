import redis
import requests
import os
from dotenv import load_dotenv
from .celery import app

load_dotenv()

redis_host = "localhost"
redis_port = 6379
redis_connection = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)



@app.task()
def sendotp(phone, otp):
    redis_connection.set(phone, otp, ex=180)
    url = "https://api.sms.ir/v1/send/verify/"
    API_KEY = os.environ.get('API-KET')
    data = {
        "mobile": phone,
        "templateId": 100000,
        "parameters": [
            {"name": "Code",
             "value": otp
             }
        ]
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "text/plain",
        "x-api-key": API_KEY
    }
    requests.post(url=url, json=data, headers=headers)


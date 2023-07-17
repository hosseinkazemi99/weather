import requests
import redis
from celery import Celery
from celery.schedules import crontab

app = Celery("task111", broker="redis://localhost@6379/0")
URL = "https://api.openweathermap.org/data/2.5/weather"
APIkey = "ac47c08e360d8994ea5d822212a2add5"
redis_host = "localhost"
redis_port = 6379
rd = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

beat_schedule = {
    "call_my_weather_every_minutes": {
        "task": "my_weathers",
        "schedule": crontab(minute="*/1"),
        "args": ("Tehran", "Shiraz", "Mashhad", "Qom", "Isfahan", "Ardabil", "Hamedan", "Yazd", "Tabriz", "Zavareh")
    }
}


@app.task()
def get_weather_status(city: str):
    cache_temp = rd.get(city)
    if cache_temp is not None:
        return cache_temp
    try:
        params = {"q": city, "appid": APIkey}
        response = requests.get(url=URL, params=params)
        temp = (response.json()['main']['temp']) - 273.15
        temp = round(temp, 1)
        rd.set(city, temp, ex=300)
        return f"{temp}C"
    except ConnectionError:
        return "We have a problem communicating with the server. Sorry"

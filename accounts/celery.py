from celery import Celery
from celery.schedules import crontab

# Create the Celery app
app = Celery('tasks')

# Load the Django settings module
app.config_from_object('django.conf:settings', namespace='CELERY')
cities = ["Tehran", "Shiraz", "Mashhad", "Qom", "Isfahan", "Ardabil", "Hamedan", "Yazd", "Tabriz", "Zavareh"]
app.conf.beat_schedule = {}
for city in cities:
    app.conf.beat_schedule[f"update_weather_{city}"] = {
        "task": "accounts.weather.get_weather_status",
        "schedule": crontab(minute="*/5"),  # Run every 5 minutes
        "args": (city,),
    }

# app.conf.beat_schedule = {
#     "update_weather_tehran": {
#         "task": "accounts.weather.get_weather_status",
#         "schedule": crontab(minute="*/5"),  # Run every 5 minutes
#         "args": ("Tehran",),
#     },
# }
# Discover and register tasks from all installed apps
app.autodiscover_tasks()


# (myenv) hossein@Tabaie:~/Makeen/makeen-tasks/hosseinTabaie/tasks/task112-otp$ DJANGO_SETTINGS_MODULE=my_site.set

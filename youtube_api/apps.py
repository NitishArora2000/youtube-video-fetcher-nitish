from apscheduler.schedulers.background import BackgroundScheduler
from django.apps import AppConfig


class YoutubeApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'youtube_api'

    def ready(self):
        from youtube_api.utils import fetch_videos
        scheduler = BackgroundScheduler()
        scheduler.add_job(fetch_videos, 'interval', seconds=20)
        scheduler.start()

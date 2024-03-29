from background_task import background

from youtube_api.utils import fetch_videos


@background(schedule=10)
def fetch_videos_task():
    fetch_videos()

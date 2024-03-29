from googleapiclient.discovery import build
from youtube_api.models import Video


def fetch_videos(api_key, search_query):
    youtube = build('youtube', 'v3', developerKey=api_key)
    search_response = youtube.search().list(
        q=search_query,
        type='video',
        part='id,snippet',
        maxResults=50
    ).execute()

    # Add videos to the database
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            video_data = search_result['snippet']
            video = Video(
                title=video_data['title'],
                description=video_data['description'],
                published_at=video_data['publishedAt'],
                thumbnail_default=video_data['thumbnails']['default']['url'],
                thumbnail_medium=video_data['thumbnails']['medium']['url'],
                thumbnail_high=video_data['thumbnails']['high']['url']
            )
            video.save()

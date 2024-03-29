from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from youtube_api.models import Video
from youtube_video_fetcher_nitish.settings import API_KEYS


def fetch_videos(api_key_index=0):
    """
    Fetches videos from YouTube API using API keys in rotation until all keys are exhausted.

    Args:
    api_key_index (int): The index of the API key to use for the API request.
    """
    if api_key_index >= len(API_KEYS):
        print("All API keys exhausted.")
        return

    print("Starting Fetch Videos Scheduler")
    try:
        api_key = API_KEYS[api_key_index]
        youtube = build('youtube', 'v3', developerKey=api_key)
        print(f"Using API key: {api_key}")

        search_response = youtube.search().list(
            q='tech|sports',
            order='date',
            type='video',
            part='id,snippet',
            publishedAfter='2024-01-01T00:00:00Z',
            maxResults=50
        ).execute()

        videos_to_save = []
        for search_result in search_response.get('items', []):
            if search_result['id']['kind'] == 'youtube#video':
                video_data = search_result['snippet']
                video = Video(
                    title=video_data.get('title', ''),
                    description=video_data.get('description', ''),
                    published_at=video_data.get('publishedAt', ''),
                    thumbnail_default=video_data['thumbnails']['default']['url'],
                    thumbnail_medium=video_data['thumbnails']['medium']['url'],
                    thumbnail_high=video_data['thumbnails']['high']['url']
                )
                videos_to_save.append(video)

        # Bulk insert videos to improve performance
        if videos_to_save:
            Video.objects.bulk_create(videos_to_save)
            print(f"Saved {len(videos_to_save)} videos.")

    except HttpError as e:
        print(f"HTTP Error: {e}")
        if e.resp.status == 403:
            print("API key exhausted. Rotating to the next key.")
            fetch_videos(api_key_index + 1)  # Rotate to the next key

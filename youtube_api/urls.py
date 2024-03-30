from django.urls import path

from youtube_api.views.video_list_view import VideoListView
from youtube_api.views.video_search_view import VideoSearchView

urlpatterns = [
    path('videos/', VideoListView.as_view(), name='video-list'),
    path('search/', VideoSearchView.as_view(), name='video-search'),
]
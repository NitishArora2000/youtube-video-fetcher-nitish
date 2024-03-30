from rest_framework import views, status
from rest_framework.response import Response

from youtube_api.serializer import VideoSerializer
from youtube_api.service.search_videos import search_videos


class VideoSearchView(views.APIView):
    def get(self, request):
        # Get the search query from the 'd' parameter in the request
        query = request.query_params.get('d')

        if not query:
            return Response({'error': 'Search query parameter "d" is required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Call the service function to search for videos
        videos = search_videos(query)

        if not videos:
            return Response({'message': 'No videos found.'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the queryset and return the response
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

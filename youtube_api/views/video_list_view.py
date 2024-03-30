from rest_framework import views, status
from rest_framework.response import Response

from youtube_api.models import Video
from youtube_api.serializer import VideoSerializer
from youtube_api.service.pagination_service import CustomCursorPagination


class VideoListView(views.APIView):
    pagination_class = CustomCursorPagination()

    def get(self, request):
        """
        Get paginated list of videos with custom cursor pagination.
        """
        paginator = self.pagination_class
        queryset = Video.objects.all()

        page_size = paginator.get_page_size(request)  # Get dynamically determined page size
        paginator.page_size = page_size  # Set the page size in the paginator

        page = paginator.paginate_queryset(queryset, request)
        serializer = VideoSerializer(page, many=True)

        response_data = {
            'results': serializer.data,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link()
        }

        return Response(response_data, status=status.HTTP_200_OK)

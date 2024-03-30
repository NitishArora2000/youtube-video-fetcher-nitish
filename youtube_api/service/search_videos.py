from django.db.models import Q
from youtube_api.models import Video


def search_videos(query):
    # Strip both double and single quotes from the query
    query = query.strip('"\'')

    # Filter videos where the title or description contains the search query
    queryset = Video.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )

    return queryset

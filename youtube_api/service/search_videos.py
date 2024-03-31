from django.db.models import Q
from youtube_api.models import Video


def search_videos(query):
    # Strip both double and single quotes from the query
    query = query.strip('"\'')

    # Split the search query into individual words and filter out any empty strings
    search_words = [word.strip() for word in query.split() if word.strip()]

    # Create Q objects for title and description separately
    title_q_objects = Q()
    description_q_objects = Q()

    for word in search_words:
        title_q_objects &= Q(title__icontains=word)
        description_q_objects &= Q(description__icontains=word)

    # Combine title and description Q objects using OR
    combined_q_objects = title_q_objects | description_q_objects

    # Filter videos based on the combined Q object
    queryset = Video.objects.filter(combined_q_objects)
    print(queryset.query)  # Debug statement to print the SQL query

    return queryset

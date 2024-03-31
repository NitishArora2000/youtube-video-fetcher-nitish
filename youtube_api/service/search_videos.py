import re

from django.db.models import Q
from youtube_api.models import Video


def search_videos(query):
    # Strip both double and single quotes from the query
    query = query.strip('"\'')

    # Split the search query into individual words and filter out any empty strings
    search_words = [word.strip() for word in query.split() if word.strip()]
    print(search_words)

    # Create a Q object for each search word in both title and description with word boundaries
    title_q_objects = [Q(title__iregex=r'\y{}\y'.format(re.escape(word))) for word in search_words]
    description_q_objects = [Q(description__iregex=r'\y{}\y'.format(re.escape(word))) for word in search_words]
    print(title_q_objects)
    print(description_q_objects)

    # Combine Q objects for title and description using &
    combined_title_q_objects = Q()
    for title_q_object in title_q_objects:
        combined_title_q_objects &= title_q_object

    combined_description_q_objects = Q()
    for description_q_object in description_q_objects:
        combined_description_q_objects &= description_q_object

    # Combine title and description Q objects using |
    combined_q_objects = combined_title_q_objects | combined_description_q_objects

    # Filter videos based on the combined Q object
    queryset = Video.objects.filter(combined_q_objects)
    print(queryset.query)  # Debug statement to print the SQL query

    return queryset

from rest_framework.pagination import CursorPagination


class CustomCursorPagination(CursorPagination):
    page_size = 10  # Default page size
    ordering = '-published_at'
    cursor_query_param = 'cursor'

    def get_page_size(self, request):
        """
        Get the page size dynamically from the request parameters.
        """
        page_size = request.GET.get('page_size')
        if page_size and page_size.isdigit():
            return int(page_size)
        return self.page_size

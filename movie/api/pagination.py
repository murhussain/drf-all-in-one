from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class WatchlistPagination(PageNumberPagination):
    page_size = 5
    # define your custom page number items size 'with just size=number
    page_size_query_param = 'size'
    # define maximum size item they can't go beyond
    max_page_size = 5


#  Normal soft don't prefer this staffs
class WatchlistPaginationOL(LimitOffsetPagination):
    default_limit = 5
    max_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'start'


class WatchlistCursorPagination(CursorPagination):
    page_size = 5
    cursor_query_param = 'records'




from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param


class StandardPagination(pagination.PageNumberPagination):
    page_size = 10
    max_page_size = 100
    page_size_query_param = "size"
    page_query_param = "page"

    def get_first_link(self):
        """Return the first page link."""
        url = self.request.build_absolute_uri()
        page_number = 1
        return replace_query_param(url, self.page_query_param, page_number)

    def get_last_link(self):
        """Return the last page link."""
        url = self.request.build_absolute_uri()
        page_number = self.page.paginator.num_pages
        return replace_query_param(url, self.page_query_param, page_number)

    def get_paginated_response(self, data):
        next_page = self.page.next_page_number() if self.page.has_next() else None
        previous_page = (
            self.page.previous_page_number() if self.page.has_previous() else None
        )

        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                    "first": self.get_first_link(),
                    "last": self.get_last_link(),
                },
                "next_page": next_page,
                "previous_page": previous_page,
                "current_page": self.page.number,
                "num_pages": self.page.paginator.num_pages,
                "num_results": self.page.paginator.count,
                # "start_index": self.page.start_index(),
                # "end_index": self.page.end_index(),
                "results": data,
            }
        )

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param, replace_query_param

class CustomPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 50
    
    def get_paginated_response(self, data):
        return Response({
            'pagination': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            
            'count': self.count,
            'results': data
        })
        


from django.db.models import Q
from rest_framework.filters import BaseFilterBackend


class PriceRangeFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        query_params = request.query_params
        from_price = query_params.get('from_price')
        to_price = query_params.get('to_price')
        if from_price and to_price:
            return queryset.filter(Q(price__gte=query_params['from_price']) & Q(price__lte=query_params['to_price']))
        return queryset

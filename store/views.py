from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import filters
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django_filters.rest_framework import DjangoFilterBackend

from store import models
from store import serializers
from store import permissions
from store.filters import PriceRangeFilterBackend
from store.throttles import TimeRateThrottle


class ShopViewSet(viewsets.ModelViewSet):
    queryset = models.Shop.objects.all()
    serializer_class = serializers.ShopSerializer
    permission_classes = [permissions.ShopAdminPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ('title',)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all().prefetch_related(
        "parents"
    )
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.CategoryAdminPermission]
    search_fields = ("uuid", "title", "parents")

    # def list(self, request, *args, **kwargs):
    #     queryset = self.queryset
    #     serializer = serializers.CategoryListRetrieveSerializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, uuid=None, *args, **kwargs):
    #     queryset = self.queryset
    #     category = get_object_or_404(queryset, uuid=uuid)
    #     serializer = serializers.CategoryListRetrieveSerializer(category)
    #     return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all().prefetch_related(
        "photos", "categories"
    ).select_related("shop")

    serializer_class = serializers.ProductSerializer

    permission_classes = (
        permissions.ProductAdminPermission,
    )
    parser_classes = (
        MultiPartParser, FormParser,
    )
    filter_backends = [DjangoFilterBackend, PriceRangeFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    throttle_classes = (AnonRateThrottle,
                        # UserRateThrottle,
                        TimeRateThrottle,
                        )
    filterset_fields = ('active', )
    search_fields = ('title', 'uuid')
    ordering_fields = ('amount', 'price',)
    autocomplete_fields = ('shop',)

    # def get_queryset(self):
    #     return super().get_queryset()[:5]

    # def list(self, request, *args, **kwargs):
    #     queryset = super().get_queryset()[:5]
    #     serializer = serializers.ProductListRetrieveSerializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, uuid=None, *args, **kwargs):
    #     queryset = self.queryset
    #     product = get_object_or_404(queryset, uuid=uuid)
    #     serializer = serializers.ProductListRetrieveSerializer(product)
    #     return Response(serializer.data)


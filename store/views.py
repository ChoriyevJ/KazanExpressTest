from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from store import models
from store import serializers
from store import permissions
from store.filters import PriceRangeFilterBackend


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
    )
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.ProductAdminPermission]
    filter_backends = [DjangoFilterBackend, PriceRangeFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ('active', )
    search_fields = ('title', 'uuid')
    ordering_fields = ('amount', 'price',)

    # def list(self, request, *args, **kwargs):
    #     queryset = self.queryset
    #     serializer = serializers.ProductListRetrieveSerializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, uuid=None, *args, **kwargs):
    #     queryset = self.queryset
    #     product = get_object_or_404(queryset, uuid=uuid)
    #     serializer = serializers.ProductListRetrieveSerializer(product)
    #     return Response(serializer.data)

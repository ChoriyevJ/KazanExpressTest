from rest_framework import serializers

from store import models


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Photo
        fields = ('image',)


class ShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Shop
        fields = ('title', 'description', 'image')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('title', 'description', 'parents')


class CategorySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('title',)


class CategoryListRetrieveSerializer(serializers.ModelSerializer):

    parents = CategorySimpleSerializer(many=True)

    class Meta:
        model = models.Category
        fields = ('title', 'description', 'parents')


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Product
        fields = ('title', 'description', 'amount', 'main_photo',
                  'price', 'active', 'photos', 'categories')


class ProductListRetrieveSerializer(serializers.ModelSerializer):

    photos = PhotoSerializer(many=True)
    categories = CategorySimpleSerializer(many=True)

    class Meta:
        model = models.Product
        fields = ('title', 'description', 'amount', 'main_photo',
                  'price', 'active', 'photos', 'categories')

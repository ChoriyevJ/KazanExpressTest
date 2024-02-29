from rest_framework import serializers

from store import models


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Photo
        fields = ('image', 'is_main')


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


class ShopTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Shop
        fields = ('title',)


class ProductSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, required=False)
    # photos = serializers.ListSerializer(
    #     child=serializers.FileField(max_length=100000000,
    #                                 allow_empty_file=False,
    #                                 use_url=False
    #                                 ))

    class Meta:
        model = models.Product
        fields = ('title', 'description', 'amount', 'main_photo',
                  'price', 'active', 'photos', 'categories', 'shop')

    def create(self, validated_data):
        photos_data = validated_data.pop('photos', [])
        product = models.Product.objects.create(**validated_data)
        for photo_data in photos_data:
            models.Photo.objects.create(product=product, **photo_data)
        return product


class ProductListRetrieveSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True)
    categories = CategorySimpleSerializer(many=True)

    class Meta:
        model = models.Product
        fields = ('title', 'description', 'amount', 'main_photo',
                  'price', 'active', 'photos', 'categories')

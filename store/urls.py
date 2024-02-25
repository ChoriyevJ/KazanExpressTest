from django.urls import path, include
from rest_framework import routers

from store import views


router = routers.DefaultRouter()
router.register('shop', views.ShopViewSet)
router.register('category', views.CategoryViewSet)
router.register('product', views.ProductViewSet)

urlpatterns = [
    path('', include(router.urls))
]


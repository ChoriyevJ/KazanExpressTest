from rest_framework import permissions


class ShopAdminPermission(permissions.BasePermission):
    message = "Yo have not a permission for shop!"

    def has_permission(self, request, view):
        return True if request.user.user_permissions.filter(codename__in=('shop_admin', 'store_admin')).exists() else False

        # return True if request.user.roles.filter(code='shop_admin').exists() else False

    def has_object_permission(self, request, view, obj):
        return True if request.user.user_permissions.filter(codename__in=('shop_admin', 'store_admin')).exists() else False


class ProductAdminPermission(permissions.BasePermission):
    message = "Yo have not a permission for product!"

    def has_permission(self, request, view):
        return True if request.user.user_permissions.filter(codename__in=('product_admin', 'store_admin')).exists() else False

        # return True if request.user.roles.filter(code__in=(['product_admin', 'store_admin])).exists() else False

    def has_object_permission(self, request, view, obj):
        return True if request.user.user_permissions.filter(codename__in=('product_admin', 'store_admin')).exists() else False


class CategoryAdminPermission(permissions.BasePermission):
    message = "Yo have not a permission for category!"

    def has_permission(self, request, view):
        return True if request.user.user_permissions.filter(codename__in=('category_admin', 'store_admin')).exists() else False

        # return True if request.user.roles.filter(code='category_admin').exists() else False

    def has_object_permission(self, request, view, obj):
        return True if request.user.user_permissions.filter(codename__in=('category_admin', 'store_admin')).exists() else False

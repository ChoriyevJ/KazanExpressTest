import uuid

from django.contrib.auth import get_user_model
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Shop(BaseModel):
    uuid = models.UUIDField(primary_key=True, max_length=8, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.title


class Category(BaseModel):
    uuid = models.UUIDField(primary_key=True, max_length=8, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    parents = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.title


class Product(BaseModel):
    uuid = models.UUIDField(primary_key=True, max_length=8, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    main_photo = models.ImageField(upload_to='images/',
                                   blank=True, null=True, editable=False)
    amount = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    active = models.BooleanField(default=True)

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE,
                             related_name='products')
    categories = models.ManyToManyField('Category', related_name='products')

    def __str__(self):
        return self.title


class Photo(BaseModel):
    image = models.ImageField(upload_to='images/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='photos')
    is_main = models.BooleanField(default=False)

    class Meta:
        unique_together = ('image', 'product')
        ordering = ['-is_main']

    def __str__(self):
        return f'{self.image}'

    def save(self, *args, **kwargs):
        if self.is_main:
            self.product.main_photo = self.image
            self.product.save()
        super().save(*args, **kwargs)


class Role(BaseModel):
    title = models.CharField(max_length=63)
    user = models.ManyToManyField(get_user_model(), related_name="roles",
                                  blank=True)
    code = models.CharField(max_length=31, blank=True, null=True)

    def __str__(self):
        return self.title

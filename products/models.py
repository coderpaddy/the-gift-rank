from django.db import models
import random

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=500)
    short_name = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    short_description = models.CharField(max_length=500)
    img_thumb = models.CharField(max_length=500)
    img_full = models.CharField(max_length=500)
    rank = models.IntegerField()
    mycategory = models.CharField(max_length=500)
    realcategory = models.CharField(max_length=500)
    subcategory = models.CharField(max_length=500)
    date = models.DateField(auto_now=True)
    pageviews = models.IntegerField(default=random.randint(1, 275))   
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    video = models.CharField(max_length=500)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.short_name

class Store(models.Model):
    name = models.CharField(max_length=500)
    rating = models.IntegerField(default=0)
    homepage = models.CharField(max_length=500)
    reflink = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class PriceLink(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="link")
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="store")
    price = models.IntegerField()
    clicks = models.IntegerField()
    url = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.product} : {self.store} : {self.price}"
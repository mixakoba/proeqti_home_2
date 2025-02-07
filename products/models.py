from django.db import models
from django.core.validators import MaxValueValidator
from config.model_utils.models import TimeStampedModel
from products.choices import Currency

class Product(TimeStampedModel, models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    currency = models.CharField(max_length=255, choices=Currency.choices, default=Currency.GEL)
    tags = models.ManyToManyField("products.ProductTag", related_name='products', blank=True)

    def __str__(self):
        return f"Product: {self.name} - {self.price} {self.currency}"

    def average_rating(self):
        pass


class Review(TimeStampedModel, models.Model):
    product = models.ForeignKey('products.Product', related_name='reviews',on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])

    def __str__(self):
        return f"Review by {self.user} for {self.product.name} - Rating: {self.rating}"


class FavoriteProduct(TimeStampedModel, models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user} favorite: {self.product.name}"


class ProductTag(TimeStampedModel, models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"Tag: {self.name}"


class Cart(TimeStampedModel, models.Model):
    products = models.ManyToManyField('products.Product', related_name='carts')
    user = models.OneToOneField('users.User', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Cart for {self.user}"


class ProductImage(TimeStampedModel, models.Model):
    image = models.ImageField(upload_to='products/')
    product = models.ForeignKey('products.Product', related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for {self.product.name}"
    
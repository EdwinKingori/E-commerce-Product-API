from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=250)


class Products(models.Model):
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField()
    unitprice = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(1)])
    stock_quantity = models.IntegerField([MinValueValidator(1)])
    image_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=250)
    birthdate = models.DateField(null=True, blank=True)
    address = models.TextField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

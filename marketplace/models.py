from django.db import models

from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
def product_directory_path(instancce,filename):
    return f"products/{instancce}/{filename}"

class Product(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    label = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    phone = PhoneNumberField()
    image = models.ImageField(upload_to=product_directory_path)
    description = models.TextField(max_length=200)
    quantity = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.label

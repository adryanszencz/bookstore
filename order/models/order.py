from django.contrib.auth.models import User
from django.db import models

from product.models import Product


class Order(models.Model):
    product = models.ManyToManyField(Product, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pedido {self.pk} de {self.user}"

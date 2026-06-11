from django.db import models
from products.models import Product
from django.contrib.auth.models import User


class CartItem(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(default=1)

    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'product')  # Prevent duplicate cart entries

    def __str__(self):
        return f'{self.user.username.capitalize()} added {self.product.title} - {self.quantity}'

    @property
    def sub_total(self):
        return self.product.price * self.quantity
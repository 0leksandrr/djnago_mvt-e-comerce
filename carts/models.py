from django.db import models
from accounts.models import Account
from store.models import Product, Variation


class Cart(models.Model):
    objects = models.Manager()
    cart_id = models.CharField(max_length=250, blank=True, verbose_name='ID кошика')
    date_added = models.DateField(auto_now_add=True, verbose_name='Дата додавання')

    def __str__(self):
        return self.cart_id

    class Meta:
        verbose_name = 'Кошик'
        verbose_name_plural = 'Кошики'


class CartItem(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, verbose_name='Користувач')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    variations = models.ManyToManyField(Variation, blank=True, verbose_name='Варіації')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, verbose_name='Кошик')
    quantity = models.IntegerField(verbose_name='Кількість')
    is_active = models.BooleanField(default=True, verbose_name='Активно')

    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product

    class Meta:
        verbose_name = 'Товар у кошику'
        verbose_name_plural = 'Товари у кошику'

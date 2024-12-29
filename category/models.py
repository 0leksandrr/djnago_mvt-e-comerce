from django.db import models
from django.urls import reverse


class Category(models.Model):
    objects = models.Manager()

    category_name = models.CharField(max_length=50, unique=True, verbose_name='Назва категорії')
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, verbose_name='Опис')
    cat_image = models.ImageField(upload_to='photos/categories', blank=True, verbose_name='Фото категорії')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='subcategories',
        blank=True,
        null=True,
        verbose_name='Батьківська категорія'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Категорію'
        verbose_name_plural = 'Категорії'

    def get_url(self):
        """
        Get category URL to use in navbar and left menu
        :return: URL for the particular category
        """
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name

    def is_root_category(self):
        """
        Check if the category is a root category (no parent).
        """
        return self.parent is None

from store.models import Product
from .models import Category


def menu_links(request):
    """
    Get links for all categories in database.
    After that we can use this links in templates anywhere in the project.
    :param request:
    :return: dictionary of links
    """
    top_level_categories = Category.objects.filter(parent__isnull=True).order_by('category_name')
    count_products_by_category = [
        len(Product.objects.filter(category=category, is_available=True)) for category in top_level_categories
    ]
    return dict(links=top_level_categories, count_products_by_category=count_products_by_category)

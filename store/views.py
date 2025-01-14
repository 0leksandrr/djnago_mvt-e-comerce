from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q, Max, Min
from django.shortcuts import render, get_object_or_404, redirect

from carts.models import CartItem
from carts.views import _cart_id
from category.models import Category
from .forms import ReviewForm
from .models import Product, ReviewRating, ProductGallery



def paginator(request, queryset, per_page):
    """
    Paginate a queryset.
    :param request: HTTP request
    :param queryset: Queryset to paginate
    :param per_page: Number of items per page
    :return: Paged queryset and page range
    """
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Обчислення діапазону сторінок для відображення
    current_page = page_obj.number
    total_pages = paginator.num_pages
    page_range = [
        i for i in range(1, total_pages + 1)
        if i == 1 or i == total_pages or (current_page - 3 <= i <= current_page + 3)
    ]

    return page_obj, page_range


def store(request, category_slug=None):
    """
    Render 'store' page where show all products or products by category in sale.
    :param request:
    :param category_slug: Category name
    :return: Render store.html
    """
    categories = None
    products = None

    # Sidebar panel (products amount, price range)
    all_products_count = Product.objects.all().count()
    max_price_placeholder = Product.objects.aggregate(Max('price'))['price__max']
    min_price_placeholder = Product.objects.aggregate(Min('price'))['price__min']

    def get_all_subcategories(category):
        """Recursively get all subcategories of a category."""
        subcategories = category.subcategories.all()
        all_subcategories = list(subcategories)
        for subcategory in subcategories:
            all_subcategories.extend(get_all_subcategories(subcategory))
        return all_subcategories

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        all_categories = [categories] + get_all_subcategories(categories)

        if 'min_price' in request.GET:
            min_price = request.GET.get('min_price') or 0
            max_price = request.GET.get('max_price') or max_price_placeholder
            products = Product.objects.filter(
                price__range=(min_price, max_price),
                category__in=all_categories,
                is_available=True
            ).order_by('id')
        else:
            products = Product.objects.filter(
                category__in=all_categories,
                is_available=True
            ).order_by('id')
    else:
        if 'min_price' in request.GET:
            min_price = request.GET.get('min_price') or 0
            max_price = request.GET.get('max_price') or max_price_placeholder
            products = Product.objects.filter(
                is_available=True,
                price__range=(min_price, max_price)
            ).order_by('id')
        else:
            products = Product.objects.filter(is_available=True).order_by('id')

    paged_products, page_range = paginator(request, products, 24)
    product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
        'all_products_count': all_products_count,
        'max_price_placeholder': max_price_placeholder,
        'min_price_placeholder': min_price_placeholder,
        'page_range': page_range
    }
    return render(request, 'store/store.html', context)



def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        order_product = None
    else:
        order_product = None

    # Get the reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    # Get the product gallery
    product_gallery = single_product.additional_images
    product_gallery_urls = [f"/media/{image}" for image in product_gallery]

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'order_product': order_product,
        'reviews': reviews,
        'product_gallery': product_gallery_urls
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    """
    Find products by keyword
    :param request:
    :return: Render 'store' page
    """
    products = None
    paged_products = None
    product_count = None
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by(
                '-created_date').filter(Q(product_name__icontains=keyword) |
                                        Q(description__icontains=keyword))
            if 'keyword' in request.GET and request.GET['keyword']:
                page = request.GET.get('page')
                keyword = request.GET['keyword']
                paginator = Paginator(products, 6)
            paged_products = paginator.get_page(page)
            product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
        'keyword': keyword
    }
    return render(request, 'store/store.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Спасибо! Ваш отзыв обновлен.')
            return redirect(url)
        except ObjectDoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Спасибо! Ваш отзыв отправлен.')
                return redirect(url)

from django.conf import settings
from django.core.cache import cache

from catalog.models import Category, Product


def get_products_from_cache():
    if not settings.CACHE_ENABLED:
        return Product.objects.all().order_by("-id")

    key = "products"
    products = cache.get(key)
    if products is None:
        products = Product.objects.all().order_by("-id")
        cache.set(key, products)
    return products


def get_categories_from_cache():
    if not settings.CACHE_ENABLED:
        return Category.objects.all()

    key = "categories"
    categories = cache.get(key)
    if categories is None:
        categories = Category.objects.all()
        cache.set(key, categories)
    return categories

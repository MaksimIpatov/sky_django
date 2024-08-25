from django.contrib import admin

from catalog.models import Category, Contact, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "price",
        "category",
    )
    list_display_links = ("title",)
    list_filter = ("category",)
    search_fields = (
        "title",
        "description",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
    )
    list_display_links = ("title",)


admin.site.register(Contact)

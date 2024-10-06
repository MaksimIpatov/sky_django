from django.contrib import admin

from catalog.models import Blog, Category, Contact, Product


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


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "views",
        "slug",
        "created_at",
    )
    fields = (
        "title",
        "description",
        "preview",
        "views",
        "is_published",
    )
    list_display_links = ("title",)
    list_filter = ("is_published",)
    search_fields = ("title",)


admin.site.register(Contact)

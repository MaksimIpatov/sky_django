from django.contrib import admin

from catalog.models import Blog, Category, Contact, Product, Version


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "price",
        "category",
        "author",
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
    list_display_links = ("title",)
    list_filter = ("is_published",)
    search_fields = ("title",)


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = (
        "build",
        "major",
        "product",
        "is_active",
    )
    list_display_links = ("build",)
    search_fields = (
        "product__name",
        "build",
    )
    list_filter = ("is_active",)


admin.site.register(Contact)

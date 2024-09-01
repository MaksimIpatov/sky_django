from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from catalog.views import (
    BlogCreateView,
    BlogDeleteView,
    BlogDetailView,
    BlogListView,
    BlogUpdateView,
    ContactView,
    IndexView,
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductListView,
    ProductUpdateView,
)

urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),
    path(
        "",
        IndexView.as_view(),
        name="index",
    ),
    path(
        "product/",
        ProductListView.as_view(),
        name="product_list",
    ),
    path(
        "product/<int:pk>",
        ProductDetailView.as_view(),
        name="product_detail",
    ),
    path(
        "product/create/",
        ProductCreateView.as_view(),
        name="product_create",
    ),
    path(
        "product/<int:pk>/update/",
        ProductUpdateView.as_view(),
        name="product_update",
    ),
    path(
        "product/<int:pk>/delete/",
        ProductDeleteView.as_view(),
        name="product_delete",
    ),
    path(
        "contacts/",
        ContactView.as_view(),
        name="contacts",
    ),
    path(
        "blog/",
        BlogListView.as_view(),
        name="blog_list",
    ),
    path(
        "blog/<int:pk>/",
        BlogDetailView.as_view(),
        name="blog_detail",
    ),
    path(
        "blog/create/",
        BlogCreateView.as_view(),
        name="blog_create",
    ),
    path(
        "blog/<int:pk>/update/",
        BlogUpdateView.as_view(),
        name="blog_update",
    ),
    path(
        "blog/<int:pk>/delete/",
        BlogDeleteView.as_view(),
        name="blog_delete",
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

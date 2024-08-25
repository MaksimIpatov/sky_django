from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from catalog.views import contacts, index, product_detail

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("product/<int:pk>", product_detail, name="product_detail"),
    path("contacts/", contacts, name="contacts")
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

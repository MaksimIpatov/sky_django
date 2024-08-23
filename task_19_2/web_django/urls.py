from django.contrib import admin
from django.urls import path

from catalog.views import contacts, index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("contacts/", contacts, name="contacts")
]

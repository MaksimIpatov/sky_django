from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "phone",
        "country",
    )
    list_display_links = ("email",)
    search_fields = (
        "email",
        "phone",
    )

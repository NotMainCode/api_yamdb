"""Admin site settings of the 'Users' application."""

from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Table settings for resource 'Users' on the admin site."""

    list_display = (
        "pk",
        "username",
        "email",
        "role",
        "first_name",
        "last_name",
        "bio",
    )
    list_editable = ("role",)
    search_fields = ("username",)
    list_filter = ("role",)

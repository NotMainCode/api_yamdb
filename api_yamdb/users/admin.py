"""Admin site settings of the 'Users' application."""

from django.contrib import admin

from users.models import User

admin.site.register(User)

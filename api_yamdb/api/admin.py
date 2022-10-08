from django.contrib import admin

from reviews.models import Categories, Genres, Title, Review

admin.site.register(Categories)
admin.site.register(Genres)
admin.site.register(Title)
admin.site.register(Review)

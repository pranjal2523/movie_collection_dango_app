from django.contrib import admin
from .models import Collection, Movie


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'uuid']
    search_fields = ['title', 'user__username']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'collection', 'genres']
    search_fields = ['title', 'genres']
    list_filter = ['collection']

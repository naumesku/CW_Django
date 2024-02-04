from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'data_create', 'is_published')
    search_fields = ('title', 'data_create',)
    list_filter = ('is_published', 'data_create')

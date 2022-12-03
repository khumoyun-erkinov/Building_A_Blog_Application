from django.contrib import admin
from .models import Post
# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','slug','author','publish','status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body'] #This codes displays title and body`s searching
    prepopulated_fields = {'slug': ('title',)} # This shows us Django administraion part of action
    raw_id_fields = ['author']
    date_hierarchy = 'publish' # This shows us when code is written,create
    ordering = ['status', 'publish']
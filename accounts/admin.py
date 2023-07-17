from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('owner_id','owner','id', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('text',)


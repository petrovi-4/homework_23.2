from django.contrib import admin

from blog.models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title')
    prepopulated_fields = {'slug': ('title',)}

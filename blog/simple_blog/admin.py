###Admin
from simple_blog.models import Post
from django.contrib import admin

class PostAdmin(admin.ModelAdmin):
	search_fields = ["title"]
	
admin.site.register(Post, PostAdmin)
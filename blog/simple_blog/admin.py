###Admin
from simple_blog.models import Post
from django.contrib import admin

class PostAdmin(admin.ModelAdmin):
	search_fields = ["title"]

class CommentAdmin(admin.ModelAdmin):
	display_fields = ["Post", "author", "created"]

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
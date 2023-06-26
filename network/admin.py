from django.contrib import admin
from .models import Post,User,Like,Comment,Follow,Chat,Message

admin.site.register(Post)
admin.site.register(User)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Chat)
admin.site.register(Message)
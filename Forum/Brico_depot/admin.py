from django.contrib import admin
from .models import CustomUser, Post, Comment, Follow, Notification, PrivateMessage

admin.site.register(CustomUser)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Notification)
admin.site.register(PrivateMessage)

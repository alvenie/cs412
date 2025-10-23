# mini_insta/admin.py
# auther: Chonghao Chen (alvenie@bu.edu), 9/25/2025
# description: The admin.py file specific to the mini insta app

from django.contrib import admin

# Register your models here.
from .models import Profile, Post, Photo, Follow, Comment, Like
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Like)

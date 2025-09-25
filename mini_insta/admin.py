# mini_insta/admin.py
# auther: Chonghao Chen (alvenie@bu.edu), 9/25/2025
# description: The admin.py file specific to the mini insta app

from django.contrib import admin

# Register your models here.
from .models import Profile
admin.site.register(Profile)

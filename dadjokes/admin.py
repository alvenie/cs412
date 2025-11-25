# dadjokes/admin.py
# auther: Chonghao Chen (alvenie@bu.edu), 11/13/2025
# description: The admin.py file specific to the dadjokes app

from django.contrib import admin
from .models import Joke, Picture

admin.site.register(Joke)
admin.site.register(Picture)
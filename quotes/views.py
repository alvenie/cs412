# file: quotes/views.py
# auther: Alven Chen (alvenie@bu.edu), 9/8/2025
# description: The views.py file specific to the quotes app

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time
import random

# Create your views here.

# Lists of quotes and images.
quote_list = ["A person who never made a mistake never tried anything new", 
              "If you can't explain it simply, you don't understand it well enough",
              "I have no special talent. I am only passionately curious."]

image_list = ["https://i.ibb.co/fYdJTNCT/albert1.jpg", "https://i.ibb.co/tTm1s3s2/albert2.jpg", "https://i.ibb.co/dJVVHMWF/albert3.jpg"]

def home_page(request):
    '''Respond to the URL '', delegate work to a template.'''

    template_name = 'quotes/home.html'
    # a dict of context variables (key-value pairs)
    context = {
        "time": time.ctime(),
        "quote": random.choice(quote_list),
        "image": random.choice(image_list),
    }
    return render(request, template_name, context)   

def quote(request):
    '''Respond to the URL 'quotes', delegate work to a template.'''

    template_name = 'quotes/quote.html'
    # a dict of context variables (key-value pairs)
    context = {
        "time": time.ctime(),
        "quote": random.choice(quote_list),
        "image": random.choice(image_list),
    }
    return render(request, template_name, context)   

def show_all(request):
    '''Respond to the URL 'show_all', delegate work to a template.'''

    template_name = 'quotes/show_all.html'
    # a dict of context variables (key-value pairs)
    context = {
        "time": time.ctime(),
        "quote": quote_list,
        "image": image_list,
    }
    return render(request, template_name, context)   

def about(request):
    '''Respond to the URL 'about', delegate work to a template.'''

    template_name = 'quotes/about.html'
    # a dict of context variables (key-value pairs)
    context = {
        "time": time.ctime(),
        "letter1": chr(random.randint(65,90)),
        "letter2": chr(random.randint(65,90)),
        "number": random.randint(1,10),
        
    }
    return render(request, template_name, context)   

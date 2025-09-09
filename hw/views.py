# file: hw/views.py

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time

# Create your views here.
def home(request):
    '''Fund to respond to the "home" request.'''

    response_text = f'''
    <html>
    <h1>Hello, World!</h1>
    The current time is {time.ctime()}.
    </html>
    '''

    return HttpResponse(response_text)

def home_page(request):
    '''Respond to the URL '', delegate work to a template.'''

    template_name = 'hw/home.html'
    return render(request, template_name)   
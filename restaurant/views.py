# formdata/views.py
# view functions to handle URL requests

from django.shortcuts import render
from django.http import HttpResponse
import time
import random

# Create your views here.
def main(request):
    '''Shows the main page of the app'''

    template_name = 'restaurant/main.html'

    context= {
        "time": time.ctime(),
    }

    return render(request, template_name=template_name, context=context)

def order(request):
    '''Shows the order page of the app'''

    template_name = 'restaurant/order.html'
    
    daily_special = [
        {
            'name': 'Gold Sauce',
            'details': 'A special rich sauce made with secret ingredients.',
            'price': 31.99,
        },
        {
            'name': 'Bacon Ranch Deluxe',
            'details': 'Signature chicken fillet topped with applewood spoked bacon.',
            'price': 31.99,
        }
    ]
    today_special = random.choice(daily_special)
    
    context= {

        "time": time.ctime(),
        'daily_special': today_special,
    }

    return render(request, template_name=template_name, context=context)


def submit(request):
    '''Process the form submission, and generating a confirmation.'''

    template_name = "restaurant/confirmation.html"

    current_time = time.time()

    random_seconds = random.uniform(30*60, 60*60)

    ready_time = current_time + random_seconds

    prices = {
        'BigMac': 8.00,
        'French Fries': 4.00,
        'Chicken Nuggets': 10.00,
        'Soda': 3.00,
        'daily_special': 31.99,
    }

    # check if POST data was sent with the HTTP POST message:
    if request.POST:

        # extract form fields into variables:
        big_mac = request.POST.get('BigMac')
        french_fries = request.POST.get('French Fries')
        chicken_nuggets = request.POST.get('Chicken Nuggets')
        soda = request.POST.get('Soda')
        # Get daily special fields
        special_name = request.POST.get('special_name')
        special_price_str = request.POST.get('special_price')
        special_instr = request.POST['special_instructions']
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']

                # Collect ordered items
        order_items = []
        total = 0
        if big_mac:
            order_items.append(('Big Mac', prices['BigMac']))
            total += prices['BigMac']
        if french_fries:
            order_items.append(('French Fries', prices['French Fries']))
            total += prices['French Fries']
        if chicken_nuggets:
            order_items.append(('Chicken Nuggets', prices['Chicken Nuggets']))
            total += prices['Chicken Nuggets']
        if soda:
            order_items.append(('Soda', prices['Soda']))
            total += prices['Soda']
        if request.POST.get('daily_special') and special_name and special_price_str:
            special_price = float(special_price_str)
            order_items.append((special_name, special_price))
            total += special_price

        context = {
            'order_items': order_items,
            'total': total,
            'special_instr': special_instr,
            'name': name,
            'phone': phone,
            'email': email,
            'r_time': time.ctime(ready_time),
        }

    # delegate the response to the template, provide context variables
    return render(request, template_name=template_name, context=context)    

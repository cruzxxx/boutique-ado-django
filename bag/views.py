from django.shortcuts import render, redirect

# Create your views here.


def view_bag(request):
    """ A view that renders the bag  contents page """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the product to the bag 
    Submit product to this view containing the product_id and the quantity"""

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')

    # Once in the view, get the bag variable if exists or create it if it doesn't
    bag = request.session.get('bag', {})

    # Add item to bag or update quantity if already exists
    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    # overwrite variable in the session with the updated version
    request.session['bag'] = bag

    return redirect(redirect_url)

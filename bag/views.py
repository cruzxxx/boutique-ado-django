from django.shortcuts import render, redirect, reverse

# Create your views here.


def view_bag(request):
    """ A view that renders the bag  contents page """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the product to the bag 
    Submit product to this view containing the product_id and the quantity"""

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None

    if 'product_size' in request.POST:
        size = request.POST['product_size']

    # Once in the view, get the bag variable if exists or create it if it doesn't
    bag = request.session.get('bag', {})

    # if there is size in the item added to bag
    if size:
        # if item is already in the bag
        if item_id in list(bag.keys()):
            # if item of same ID and size already exists in the bag, increment quantity
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
            else:
                bag[item_id]['items_by_size'][size] = quantity
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}

    # if there is no size in the item added to bag
    else:
        # Add item to bag or update quantity if already exists
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity

    # overwrite variable in the session with the updated version
    request.session['bag'] = bag

    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
    else:
        if quantity > 0:
            bag[item_id] = quantity
        else:
            bag.pop(item_id)

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""

    try:
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
        else:
            bag.pop(item_id)

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)

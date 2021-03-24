from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product

# Create your views here.


def all_products(request):
    """ A view to search all products, including sorting and search queries """

    products = Product.objects.all()
    # initialising variable query
    query = None

    if request.GET:
        # if q is in the request, store it in a variable query
        if 'q' in request.GET:
            query = request.GET['q']
            # if query is blank, return error message, then redirect back to product url
            if not query:
                messages.error(request, "You didn't enter any search criteria")
                return redirect(reverse('products'))

            # if query has a value, search for product and description using Q
            # i in front of contains make the it case insensitive
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product detail page """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)

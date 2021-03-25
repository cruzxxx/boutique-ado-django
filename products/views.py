from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category

# Create your views here.


def all_products(request):
    """ A view to search all products, including sorting and search queries """

    products = Product.objects.all()
    # initialising variable query
    query = None
    categories = None
    sort = None
    direction = None

    ''' The double underscore syntax
    is common when making queries in django (e.g. category__name__in)
    Using it here means we're looking for the name field of the category model.
    And we're able to do this because category and
    product are related with a foreign key.'''

    if request.GET:
        if 'sort' in request.GET:
            # store value of URL in the variable sortkey
            sortkey = request.GET['sort']
            # replace value of sort with value above
            sort = sortkey
            # allow case insensitive sort on the name field
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))


            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            
            products = products.order_by(sortkey)

        # checking for category in get request (URL)
        if 'category' in request.GET:
            # store value of URL in the variable categories, remove comma
            categories = request.GET['category'].split(',')
            # search for products whose category name is in the list
            products = products.filter(category__name__in=categories)
            # display categories the user selected
            categories = Category.objects.filter(name__in=categories)


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

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product detail page """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)

from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    # prevent user to access checkout by typing the url
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51IbW9zEBxn6z6QV6Uy89nmlfKyeicwc46p1EPbBGBLF26wPCXfdC7vLujqwMm2une2j8Vbph9qcLURRvIliNbSqm003FaX7gv5',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)

from django import template

# instance of template.library
register = template.Library()


# use the register filter decorator to register our
# function as a template filter. Check django doc, look up for tempalte tags and filters.
@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    return price * quantity

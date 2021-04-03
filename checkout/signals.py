'''
built-in feature of django called signals. Post, in this case, means after.
So this implies these signals are sent by django to the entire application
after a model instance is saved and after it's deleted respectively.
To receive these signals we can import receiver from django.dispatch.
Of course since we'll be listening for signals from the OrderLineItem model
we'll also need that.
'''

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderLineItem


"""
And it'll take in parameters of sender, instance, created,
and keyword arguments.
This is a special type of function which will
handle signals from the post_save event.
these parameters refer to the sender of the signal.
In our case OrderLineItem.
The actual instance of the model that sent it.
A boolean sent by django referring to whether this
is a new instance or one being updated.
And any keyword arguments.
"""

@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    instance.order.update_total()



'''
Now to execute this function anytime the post_save signal is sent.
I'll use the receiver decorator. Telling it we're receiving post saved signals.
From the OrderLineItem model.
'''


@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem delete
    """
    print('delete signal received')
    instance.order.update_total()


from django.dispatch import receiver
from shopify.signals import order_created


@receiver(order_created)
def on_order_created(sender, **kwargs):
    print(kwargs['order'])
    order = kwargs.get('order')
    if order:
        print(f"Order created successfully! Details: {order}")
    else:
        print(f"Order created signal received, but no details provided!")

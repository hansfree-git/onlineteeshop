from django.core.management.base import BaseCommand
from cart import cart

class Command(BaseCommand):
    help = "Delete shopping cart items more than 90 days old"
    def handle(self, **options):
        cart.remove_old_cart_items()

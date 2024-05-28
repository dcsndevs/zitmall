from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Set quantities to zero for products with status set to Draft'

    def handle(self, *args, **kwargs):
        draft_products = Product.objects.filter(status=0)
        updated_count = draft_products.update(quantity=0)
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated_count} products with status "Draft" to have quantity zero'))

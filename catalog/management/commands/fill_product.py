import json

from django.core.management import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        Product.objects.all().delete()

        with open('catalog_data.json') as file:
            list_of_fixture = json.load(file)
            list_product = []
            for item in list_of_fixture:
                if item['model'] == 'catalog.product':
                    category_pk = item['fields']['category']
                    item['fields']['category'] = Category.objects.get(
                        pk=category_pk)
                    list_product.append(item['fields'])

        product_for_create = []
        for category_item in list_product:
            product_for_create.append(
                Product(**category_item)
            )

        Product.objects.bulk_create(product_for_create)

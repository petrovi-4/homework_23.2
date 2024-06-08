import json

from django.core.management import BaseCommand

from catalog.models import Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        Category.objects.all().delete()

        with open('catalog_data.json') as file:
            list_of_fixture = json.load(file)
            list_category = []
            for item in list_of_fixture:
                if item['model'] == 'catalog.category':
                    list_category.append(item['fields'])

        category_for_create = []
        for category_item in list_category:
            category_for_create.append(Category(**category_item))

        Category.objects.bulk_create(category_for_create)
import json

from django.core.management import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Загружает данные категорий и продуктов из JSON файлов."

    @staticmethod
    def json_read_categories():
        with open("data/categories.json", "r", encoding="UTF-8") as file:
            return json.load(file)

    @staticmethod
    def json_read_products():
        with open("data/products.json", "r", encoding="UTF-8") as file:
            return json.load(file)

    def _get_categories_to_create(self):
        return [
            Category(
                pk=data["pk"],
                title=data["fields"]["title"],
                description=data["fields"]["description"],
            )
            for data in self.json_read_categories()
        ]

    def _get_products_to_create(self):
        return [
            Product(
                pk=data["pk"],
                title=data["fields"]["title"],
                description=data["fields"]["description"],
                image=data["fields"]["image"],
                price=data["fields"]["price"],
                category=Category.objects.get(pk=data["fields"]["category"]),
            )
            for data in Command.json_read_products()
        ]

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        Category.objects.bulk_create(self._get_categories_to_create())
        Product.objects.bulk_create(self._get_products_to_create())

        self.stdout.write(self.style.SUCCESS("Данные успешно загружены"))

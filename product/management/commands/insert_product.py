from django.core.management.base import BaseCommand
from faker import Faker
from product.models import Product, Category
import random,time,requests


class Command(BaseCommand):
    help = "Inserting dummy data"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        category_list = [
            "Digital Goods",
            "Clothing",
            "Books",
            "Sports",
            "Supermarket"
        ]

        for name in category_list:
            category, created = Category.objects.get_or_create(
                name=name,
                description=self.fake.paragraph(nb_sentences=5)
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Category created: {category.name}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Category already exists: {category.name}"))

            for _ in range(6):
                image_url = f"https://randomuser.me/api/portraits/men/{self.fake.random_int(1, 100)}.jpg"
                product = Product.objects.create(
                    category=category,
                    name=self.fake.name(),
                    description=self.fake.paragraph(nb_sentences=5),
                    price=self.fake.random_number(digits=5),
                    stock=self.fake.random_int(min=0, max=100),
                    image = image_url
                )

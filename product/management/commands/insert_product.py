from django.core.management.base import BaseCommand
from faker import Faker
from product.models import Product, Category
import random, requests
from django.conf import settings

class Command(BaseCommand):
    help = "Inserting dummy data"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def get_random_product_image(self):
        # RANDOM_USER_API_URL = "https://randomuser.me/api/portraits/men/"
        random_number = random.randint(1, 100)  # ایجاد یک عدد تصادفی برای انتخاب تصویر
        # return image_url
        return f"https://placehold.co/250x250?text=Product+{random_number}"

    def handle(self, *args, **options):
        category_list = ["Digital Goods", "Clothing", "Books", "Sports", "Supermarket"]

        for name in category_list:
            category, created = Category.objects.get_or_create(
                name=name, description=self.fake.paragraph(nb_sentences=5)
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ دسته جدید ایجاد شد: {category.name}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"ℹ️ دسته از قبل وجود دارد: {category.name}"))

            for _ in range(6):
                image_url = self.get_random_product_image()

                Product.objects.create(
                    category=category,
                    name=self.fake.name(),
                    description=self.fake.paragraph(nb_sentences=5),
                    price=self.fake.random_number(digits=5),
                    stock=self.fake.random_int(min=0, max=100),
                    external_image_url=image_url  # لینک تصویر شخص
                )

                self.stdout.write(self.style.SUCCESS(f"🛒 محصول ایجاد شد: {image_url}"))

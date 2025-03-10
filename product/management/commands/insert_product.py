from django.core.management.base import BaseCommand
from faker import Faker
from product.models import Product, Category


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
            # استفاده از get_or_create برای جلوگیری از تکراری بودن دسته‌بندی‌ها
            category, created = Category.objects.get_or_create(
                name=name,
                description=self.fake.paragraph(nb_sentences=5)
            )
            # در صورتی که دسته‌بندی جدید ایجاد شود، پیامی به کنسول چاپ می‌شود
            if created:
                self.stdout.write(self.style.SUCCESS(f"Category created: {category.name}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Category already exists: {category.name}"))

            # برای هر دسته‌بندی ۶ محصول جدید ایجاد می‌شود
            for _ in range(6):
                # محصول جدید با اطلاعات تصادفی ایجاد می‌شود
                product = Product.objects.create(
                    category=category,  # استفاده از دسته‌بندی فعلی
                    name=' '.join(self.fake.words()),  # اتصال کلمات برای نام محصول
                    description=self.fake.paragraph(nb_sentences=5),
                    price=self.fake.random_number(digits=5),
                    stock=self.fake.random_int(min=0, max=100)
                )
                self.stdout.write(self.style.SUCCESS(f"Product created: {product.name}"))

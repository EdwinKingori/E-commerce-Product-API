import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from shopify.models import Product, Category, Order, Customer


# generating data for the database to use for testing the admin configurations

User = get_user_model()


class Command(BaseCommand):
    help = 'Generate test data for the database'

    def handle(self, *args, **kwargs):
        fake = Faker()
        categories = ["Electronics", "Clothing",
                      "Books", "Home & Kitchen", "Sports"]

        # generate categories data
        for category_name in categories:
            Category.objects.get_or_create(name=category_name)

        # initiate existing users set to keep track of existing emails
        # and generate users and customers
        customers_created = 0
        existing_users = User.objects.all()
        user_emails = {user.email for user in existing_users}

        while customers_created < 50:  # Create 50 customers
            email = fake.unique.email()
            if email not in user_emails:
                user = User.objects.create_user(
                    username=fake.user_name(),
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    password='password123',  # Use a default password for testing
                    email=email
                )
                user_emails.add(email)

                if not hasattr(user, 'customer'):
                    Customer.objects.create(
                        user=user,
                        phone=fake.phone_number(),
                        birthdate=fake.date_of_birth(),
                        address=fake.address()
                    )
                    customers_created += 1

        # generate products data
        for _ in range(100):
            category = random.choice(Category.objects.all())

            Product.objects.create(
                name=fake.word().capitalize(),
                description=fake.sentence(),
                unitprice=round(random.uniform(10.0, 1000.0), 2),
                category=category
            )

        # generate Orders data
        for _ in range(100):
            product = random.choice(Product.objects.all())
            customer = random.choice(Customer.objects.all())
            payment_status = random.choice(
                [Order.PAYMENT_STATUS_PENDING, Order.PAYMENT_STATUS_COMPLETE, Order.PAYMENT_STATUS_FAILED])

            Order.objects.create(
                product=product,
                place_at=fake.date_time_this_year(),
                customer=customer,
                payment_status=payment_status
            )

        self.stdout.write(self.style.SUCCESS(
            'Successfully generated 100 products, 50 customers, and 100 orders.'))

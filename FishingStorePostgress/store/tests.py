from itertools import product
from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.
from .models import Customer, Product, ShippingAddress


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create()
        Product.objects.create(name='name', price='10')

    def test_name(self):
        product = Product.objects.get(id=1)
        field_label = Product._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_price(self):
        product = Product.objects.get(id=1)
        price = Product._meta.get_field('price').verbose_name
        self.assertEqual(price, 'price')


class ShippingAddressModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create()
        ShippingAddress.objects.create(address='address', city='city', state='state', zipcode='zipcode')

    def test_address(self):
        shipping_address = ShippingAddress.objects.get(id=1)
        address = ShippingAddress._meta.get_field('address').verbose_name
        self.assertEqual(address, 'address')

    def test_address_max_length(self):
        shipping_address = ShippingAddress.objects.get(id=1)
        max_length = ShippingAddress._meta.get_field('address').max_length
        self.assertEqual(max_length, 200)

    def test_city(self):
        shipping_address = ShippingAddress.objects.get(id=1)
        city = ShippingAddress._meta.get_field('city').verbose_name
        self.assertEqual(city, 'city')

    def test_city_max_length(self):
        shipping_address = ShippingAddress.objects.get(id=1)
        max_length = ShippingAddress._meta.get_field('city').max_length
        self.assertEqual(max_length, 200)

    def test_state(self):
        shipping_address = ShippingAddress.objects.get(id=1)
        state = ShippingAddress._meta.get_field('state').verbose_name
        self.assertEqual(state, 'state')

    def test_state_max_length(self):
        shipping_address = ShippingAddress.objects.get(id=1)
        max_length = ShippingAddress._meta.get_field('state').max_length
        self.assertEqual(max_length, 200)

    def test_zipcode(self):
        shipping_address = ShippingAddress.objects.get(id=1)
        zipcode = ShippingAddress._meta.get_field('zipcode').verbose_name
        self.assertEqual(zipcode, 'zipcode')

    def test_zipcode_max_length(self):
        shipping_address = ShippingAddress.objects.get(id=1)
        max_length = ShippingAddress._meta.get_field('zipcode').max_length
        self.assertEqual(max_length, 200)

class CustomerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create()
        Customer.objects.create(name='name', email='email')

    def test_name(self):
        customer = Customer.objects.get(id=1)
        name = Customer._meta.get_field('name').verbose_name
        self.assertEqual(name, 'name')

    def test_name_max_length(self):
        customer = Customer.objects.get(id=1)
        max_length = Customer._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_email(self):
        customer = Customer.objects.get(id=1)
        email = Customer._meta.get_field('email').verbose_name
        self.assertEqual(email, 'email')

    def test_email_max_length(self):
        customer = Customer.objects.get(id=1)
        max_length = Customer._meta.get_field('email').max_length
        self.assertEqual(max_length, 200)

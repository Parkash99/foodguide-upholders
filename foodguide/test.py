from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import MenuItem, Order


class LoginTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_success(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertRedirects(response, reverse('dashboard'))  # Redirects to the dashboard

    def test_login_failure(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)  # Renders the login page
        self.assertContains(response, 'Invalid credentials')  # Displays error message


class SignupTestCase(TestCase):
    def test_signup_success(self):
        response = self.client.post(reverse('signup'), {'username': 'newuser', 'password': 'newpassword', 'confirm_password': 'newpassword'})
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertRedirects(response, reverse('dashboard'))  # Redirects to the dashboard

    def test_signup_failure(self):
        response = self.client.post(reverse('signup'), {'username': 'newuser', 'password': 'newpassword', 'confirm_password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)  # Renders the signup page
        self.assertContains(response, 'Passwords do not match.')  # Displays error message



class PlaceOrderTestCase(TestCase):
    def setUp(self):
        self.menu_item = MenuItem.objects.create(title='Item', price=10.0)

    def test_place_order_success(self):
        response = self.client.post(reverse('place_order'), {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '1234567890',
            'item_name': 'Item',
            'quantity': 2,
            'address': '123 Street',
        })
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertRedirects(response, reverse('order_success'))  # Redirects to the order success page
        self.assertEqual(Order.objects.count(), 1)  # Creates a new order

    def test_place_order_invalid_request(self):
        response = self.client.get(reverse('place_order'))
        self.assertEqual(response.status_code, 400)  # Returns bad request status code


class RateOrderTestCase(TestCase):
    def setUp(self):
        self.order = Order.objects.create(order_id='123456', name='John Doe', email='john@example.com', phone='1234567890', item_name='Item', quantity=2, address='123 Street')

    def test_rate_order_success(self):
        response = self.client.post(reverse('rate_order'), {'rating': 4}, session={'order_id': '123456'})
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertRedirects(response, reverse('dashboard'))  # Redirects to the dashboard
        self.order.refresh_from_db()
        self.assertEqual(self.order.star_rating, 4)  # Updates the order rating

    def test_rate_order_invalid_order(self):
        response = self.client.post(reverse('rate_order'), {'rating': 4}, session={'order_id': 'invalid_order_id'})
        self.assertEqual(response.status_code, 400)  # Returns bad request status code


class IndexTestCase(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)  # Renders the index page


class MenuTestCase(TestCase):
    def setUp(self):
        self.menu_item = MenuItem.objects.create(title='Item', price=10.0)

    def test_menu_view(self):
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 200)  # Renders the menu page
        self.assertContains(response, 'Item')  # Displays the menu item


class LogoutTestCase(TestCase):
    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertRedirects(response, reverse('index'))  # Redirects to the index page

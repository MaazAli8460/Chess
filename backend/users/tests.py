from django.test import TestCase
from django.urls import reverse

from .models import User


class UserViewsTests(TestCase):
	def test_signup_page_loads(self):
		response = self.client.get(reverse("users:signup"))
		self.assertEqual(response.status_code, 200)

	def test_profile_requires_authentication(self):
		response = self.client.get(reverse("users:profile"))
		self.assertEqual(response.status_code, 302)

	def test_profile_page_loads_when_authenticated(self):
		user = User.objects.create_user(username="u1", password="pass12345")
		self.client.force_login(user)
		response = self.client.get(reverse("users:profile"))
		self.assertEqual(response.status_code, 200)

	def test_logout_redirects_to_dashboard_home(self):
		user = User.objects.create_user(username="u2", password="pass12345")
		self.client.force_login(user)
		response = self.client.post(reverse("logout"))
		self.assertRedirects(response, reverse("dashboard:home"))

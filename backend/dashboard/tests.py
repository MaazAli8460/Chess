from django.test import TestCase
from django.urls import reverse

from users.models import User


class DashboardViewsTests(TestCase):
	def test_home_page_loads(self):
		response = self.client.get(reverse("dashboard:home"))
		self.assertEqual(response.status_code, 200)

	def test_student_dashboard_requires_login(self):
		response = self.client.get(reverse("dashboard:student-dashboard"))
		self.assertEqual(response.status_code, 302)

	def test_student_dashboard_loads_for_authenticated_user(self):
		user = User.objects.create_user(username="dash-user", password="pass12345")
		self.client.force_login(user)
		response = self.client.get(reverse("dashboard:student-dashboard"))
		self.assertEqual(response.status_code, 200)

	def test_public_pages_render_without_server_errors(self):
		urls = [
			reverse("dashboard:home"),
			reverse("courses:list"),
			reverse("login"),
			reverse("users:signup"),
		]
		for url in urls:
			with self.subTest(url=url):
				response = self.client.get(url)
				self.assertLess(response.status_code, 500)

	def test_authenticated_pages_render_without_server_errors(self):
		user = User.objects.create_user(username="dash-smoke", password="pass12345")
		self.client.force_login(user)

		urls = [
			reverse("dashboard:student-dashboard"),
			reverse("users:profile"),
			reverse("chesslab:analyzer"),
			reverse("payments:plans"),
		]
		for url in urls:
			with self.subTest(url=url):
				response = self.client.get(url)
				self.assertLess(response.status_code, 500)

	def test_testimonial_admin_requires_staff(self):
		user = User.objects.create_user(username="regular-user", password="pass12345")
		self.client.force_login(user)
		response = self.client.get(reverse("dashboard:testimonial-admin"))
		self.assertEqual(response.status_code, 302)

	def test_testimonial_admin_allows_staff(self):
		staff_user = User.objects.create_user(
			username="staff-user",
			password="pass12345",
			is_staff=True,
		)
		self.client.force_login(staff_user)
		response = self.client.get(reverse("dashboard:testimonial-admin"))
		self.assertEqual(response.status_code, 200)

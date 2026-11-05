from django.test import TestCase
from django.urls import reverse

from blog.models import Article
from courses.models import Course, Enrollment, LessonProgress
from decimal import Decimal
from unittest.mock import patch

from django.http import HttpResponse
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

	def test_analytics_dashboard_renders_top_courses(self):
		staff_user = User.objects.create_user(
			username="analytics-staff",
			password="pass12345",
			is_staff=True,
		)
		course = Course.objects.create(
			title="Analytics Course",
			description="Test course",
			price=Decimal("0.00"),
			created_by=staff_user,
		)
		student = User.objects.create_user(username="analytics-student", password="pass12345")
		enrollment = Enrollment.objects.create(student=student, course=course)
		lesson = course.lessons.create(title="Lesson", content="Content")
		LessonProgress.objects.create(enrollment=enrollment, lesson=lesson, is_completed=True)

		self.client.force_login(staff_user)
		with patch("dashboard.admin_views.render", return_value=HttpResponse()):
			response = self.client.get(reverse("admin-analytics"))

		self.assertEqual(response.status_code, 200)


class OperationsWorkspaceTests(TestCase):
	def setUp(self):
		self.staff_user = User.objects.create_user(
			username="ops-staff",
			password="pass12345",
			is_staff=True,
		)
		self.client.force_login(self.staff_user)

	def test_operations_workspace_is_staff_only(self):
		self.client.logout()
		self.assertEqual(self.client.get(reverse("dashboard:operations")).status_code, 302)

	def test_staff_can_create_course_and_article_from_workspace(self):
		with patch("dashboard.operations.render", return_value=HttpResponse()):
			course_response = self.client.post(
				reverse("dashboard:operations-course-new"),
				{
					"title": "Operations Course",
					"description": "A course created from the workspace.",
					"difficulty": Course.BEGINNER,
					"price": "0.00",
					"is_published": "on",
				},
			)
		self.assertEqual(course_response.status_code, 302)
		course = Course.objects.get(title="Operations Course")
		self.assertEqual(course.created_by, self.staff_user)

		with patch("dashboard.operations.render", return_value=HttpResponse()):
			article_response = self.client.post(
				reverse("dashboard:operations-article-new"),
				{
					"title": "A Practical Article",
					"author": self.staff_user.id,
					"body": "Useful chess ideas for this week.",
					"meta_description": "Useful chess ideas.",
					"is_published": "on",
				},
			)
		self.assertEqual(article_response.status_code, 302)
		self.assertTrue(Article.objects.filter(title="A Practical Article").exists())

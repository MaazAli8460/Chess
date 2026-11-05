from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from users.models import User

from .models import Course, Enrollment, Lesson


class CourseFlowTests(TestCase):
	def setUp(self):
		self.instructor = User.objects.create_user(
			username="instructor-test",
			password="pass12345",
			role=User.INSTRUCTOR,
		)
		self.student = User.objects.create_user(username="student-test", password="pass12345")
		self.course = Course.objects.create(
			title="Tactical Basics",
			description="Test course",
			difficulty=Course.BEGINNER,
			price=Decimal("0.00"),
			is_published=True,
			created_by=self.instructor,
		)

	def test_course_list_loads(self):
		response = self.client.get(reverse("courses:list"))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Tactical Basics")

	def test_enroll_flow(self):
		self.client.force_login(self.student)
		response = self.client.post(reverse("courses:enroll", args=[self.course.slug]))
		self.assertEqual(response.status_code, 302)
		self.assertTrue(Enrollment.objects.filter(student=self.student, course=self.course).exists())

	def test_premium_course_api_hides_lessons_from_anonymous_users(self):
		premium_course = Course.objects.create(
			title="Premium Tactics",
			description="Premium test course",
			price=Decimal("19.00"),
			created_by=self.instructor,
		)
		Lesson.objects.create(course=premium_course, title="Secret lesson", content="Private content")

		response = self.client.get(reverse("courses:api-detail", args=[premium_course.slug]))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json()["lessons"], [])

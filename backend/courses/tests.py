from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from users.models import User

from .models import Course, Enrollment


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

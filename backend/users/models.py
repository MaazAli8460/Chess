from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	STUDENT = "student"
	INSTRUCTOR = "instructor"
	ADMIN = "admin"

	ROLE_CHOICES = [
		(STUDENT, "Student"),
		(INSTRUCTOR, "Instructor"),
		(ADMIN, "Admin"),
	]

	role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)
	chess_com_username = models.CharField(max_length=100, blank=True)
	bio = models.TextField(blank=True)
	is_email_verified = models.BooleanField(default=False)

	def __str__(self) -> str:
		return self.username

	@property
	def can_author_courses(self) -> bool:
		return self.role in {self.INSTRUCTOR, self.ADMIN} or self.is_staff

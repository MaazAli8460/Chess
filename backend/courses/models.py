from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
	name = models.CharField(max_length=120, unique=True)
	slug = models.SlugField(max_length=140, unique=True, blank=True)

	class Meta:
		ordering = ["name"]
		verbose_name_plural = "categories"

	def __str__(self) -> str:
		return self.name

	def save(self, *args, **kwargs) -> None:
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)


class Course(models.Model):
	BEGINNER = "beginner"
	INTERMEDIATE = "intermediate"
	ADVANCED = "advanced"

	DIFFICULTY_CHOICES = [
		(BEGINNER, "Beginner"),
		(INTERMEDIATE, "Intermediate"),
		(ADVANCED, "Advanced"),
	]

	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=220, unique=True, blank=True)
	description = models.TextField()
	category = models.ForeignKey(
		Category,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name="courses",
	)
	difficulty = models.CharField(
		max_length=20,
		choices=DIFFICULTY_CHOICES,
		default=BEGINNER,
	)
	price = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("0.00"))
	is_premium = models.BooleanField(default=False)
	is_published = models.BooleanField(default=True)
	created_by = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name="created_courses",
	)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self) -> str:
		return self.title

	def save(self, *args, **kwargs) -> None:
		if not self.slug:
			self.slug = slugify(self.title)
		self.is_premium = self.price > 0
		super().save(*args, **kwargs)

	@property
	def lessons_count(self) -> int:
		return self.lessons.count()


class Lesson(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
	title = models.CharField(max_length=200)
	order = models.PositiveIntegerField(default=1)
	content = models.TextField()
	video_url = models.URLField(blank=True)
	fen_start = models.CharField(max_length=120, blank=True)
	pgn_example = models.TextField(blank=True)
	is_free_preview = models.BooleanField(default=False)
	estimated_minutes = models.PositiveIntegerField(default=10)

	class Meta:
		ordering = ["order"]
		unique_together = ("course", "order")

	def __str__(self) -> str:
		return f"{self.course.title} - {self.title}"


class Enrollment(models.Model):
	student = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name="enrollments",
	)
	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
	enrolled_at = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)
	completed_at = models.DateTimeField(null=True, blank=True)

	class Meta:
		unique_together = ("student", "course")
		ordering = ["-enrolled_at"]

	def __str__(self) -> str:
		return f"{self.student.username} enrolled in {self.course.title}"

	@property
	def completion_percent(self) -> int:
		total = self.course.lessons.count()
		if total == 0:
			return 0
		completed = self.lesson_progress.filter(is_completed=True).count()
		return int((completed / total) * 100)


class LessonProgress(models.Model):
	enrollment = models.ForeignKey(
		Enrollment,
		on_delete=models.CASCADE,
		related_name="lesson_progress",
	)
	lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="progress_records")
	is_completed = models.BooleanField(default=False)
	last_viewed_at = models.DateTimeField(auto_now=True)
	completed_at = models.DateTimeField(null=True, blank=True)

	class Meta:
		unique_together = ("enrollment", "lesson")
		ordering = ["lesson__order"]

	def __str__(self) -> str:
		return f"{self.enrollment.student.username} - {self.lesson.title}"

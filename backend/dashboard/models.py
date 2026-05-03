from django.db import models


class Testimonial(models.Model):
	name = models.CharField(max_length=120)
	title = models.CharField(max_length=140, blank=True)
	quote = models.TextField()
	rating = models.PositiveSmallIntegerField(default=5)
	is_published = models.BooleanField(default=True)
	sort_order = models.PositiveSmallIntegerField(default=1)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["sort_order", "-created_at"]

	def __str__(self) -> str:
		return f"{self.name} ({self.rating}/5)"

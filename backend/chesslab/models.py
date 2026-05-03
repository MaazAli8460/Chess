from django.conf import settings
from django.db import models


class AnalysisHistory(models.Model):
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name="analysis_history",
	)
	fen = models.CharField(max_length=120)
	best_move = models.CharField(max_length=20, blank=True)
	evaluation = models.CharField(max_length=50, blank=True)
	source = models.CharField(max_length=50, default="fallback")
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self) -> str:
		return f"{self.user.username} - {self.fen[:20]}"

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


class SavedGame(models.Model):
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name="saved_games",
	)
	title = models.CharField(max_length=150, default="Sparring Session")
	fen = models.CharField(max_length=120)
	pgn = models.TextField(blank=True)
	result = models.CharField(max_length=50, default="In Progress")
	moves_count = models.PositiveIntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self) -> str:
		return f"{self.user.username} - {self.title} ({self.created_at:%b %d, %Y})"

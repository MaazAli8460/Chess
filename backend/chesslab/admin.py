from django.contrib import admin

from .models import AnalysisHistory


@admin.register(AnalysisHistory)
class AnalysisHistoryAdmin(admin.ModelAdmin):
	list_display = ("user", "best_move", "evaluation", "source", "created_at")
	list_filter = ("source",)

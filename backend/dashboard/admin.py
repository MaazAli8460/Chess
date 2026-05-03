from django.contrib import admin

from .models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
	list_display = ("name", "title", "rating", "is_published", "sort_order", "created_at")
	list_filter = ("is_published", "rating")
	search_fields = ("name", "title", "quote")
	ordering = ("sort_order", "-created_at")

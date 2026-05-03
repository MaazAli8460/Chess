from django.contrib import admin

from .models import Category, Course, Enrollment, Lesson, LessonProgress


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("name", "slug")
	prepopulated_fields = {"slug": ("name",)}


class LessonInline(admin.TabularInline):
	model = Lesson
	extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
	list_display = ("title", "difficulty", "price", "is_published", "created_by")
	list_filter = ("difficulty", "is_published", "is_premium")
	prepopulated_fields = {"slug": ("title",)}
	inlines = [LessonInline]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
	list_display = ("student", "course", "enrolled_at", "is_active")
	list_filter = ("is_active",)


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
	list_display = ("enrollment", "lesson", "is_completed", "last_viewed_at")
	list_filter = ("is_completed",)

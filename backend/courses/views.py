from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import generics

from payments.models import UserSubscription

from .forms import CourseForm
from .models import Course, Enrollment, Lesson, LessonProgress
from .serializers import CourseSerializer


def _has_active_subscription(user) -> bool:
	if not user.is_authenticated:
		return False
	return UserSubscription.objects.filter(
		user=user,
		status=UserSubscription.STATUS_ACTIVE,
	).exists()


def course_list_view(request: HttpRequest) -> HttpResponse:
	courses = (
		Course.objects.filter(is_published=True)
		.select_related("category", "created_by")
		.order_by("title")
	)
	return render(request, "courses/course_list.html", {"courses": courses})


def course_detail_view(request: HttpRequest, slug: str) -> HttpResponse:
	course = get_object_or_404(
		Course.objects.prefetch_related(
			Prefetch("lessons", queryset=Lesson.objects.order_by("order"))
		),
		slug=slug,
		is_published=True,
	)

	is_enrolled = False
	if request.user.is_authenticated:
		is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()

	context = {
		"course": course,
		"is_enrolled": is_enrolled,
		"can_access_premium": is_enrolled or _has_active_subscription(request.user),
	}
	return render(request, "courses/course_detail.html", context)


@login_required
def enroll_course_view(request: HttpRequest, slug: str) -> HttpResponse:
	course = get_object_or_404(Course, slug=slug, is_published=True)
	if request.method != "POST":
		return redirect("courses:detail", slug=course.slug)

	if course.is_premium and not _has_active_subscription(request.user):
		messages.error(request, "This is a premium course. Activate a subscription first.")
		return redirect("payments:plans")

	_, created = Enrollment.objects.get_or_create(student=request.user, course=course)
	if created:
		messages.success(request, "You are now enrolled in this course.")
	else:
		messages.info(request, "You are already enrolled.")

	first_lesson = course.lessons.order_by("order").first()
	if first_lesson:
		return redirect("courses:lesson", slug=course.slug, lesson_id=first_lesson.id)
	return redirect("courses:detail", slug=course.slug)


@login_required
def lesson_detail_view(request: HttpRequest, slug: str, lesson_id: int) -> HttpResponse:
	course = get_object_or_404(Course, slug=slug, is_published=True)
	lesson = get_object_or_404(Lesson, id=lesson_id, course=course)

	enrollment = Enrollment.objects.filter(student=request.user, course=course).first()
	if not enrollment and not lesson.is_free_preview:
		messages.error(request, "Enroll in this course to unlock all lessons.")
		return redirect("courses:detail", slug=course.slug)

	progress = None
	if enrollment:
		progress, _ = LessonProgress.objects.get_or_create(enrollment=enrollment, lesson=lesson)
		if request.method == "POST":
			progress.is_completed = True
			from django.utils import timezone

			progress.completed_at = timezone.now()
			progress.save(update_fields=["is_completed", "completed_at", "last_viewed_at"])
			messages.success(request, "Great work! Lesson marked complete.")
			return redirect("courses:lesson", slug=course.slug, lesson_id=lesson.id)

	all_lessons = list(course.lessons.order_by("order"))
	index = all_lessons.index(lesson)
	previous_lesson = all_lessons[index - 1] if index > 0 else None
	next_lesson = all_lessons[index + 1] if index + 1 < len(all_lessons) else None

	context = {
		"course": course,
		"lesson": lesson,
		"progress": progress,
		"previous_lesson": previous_lesson,
		"next_lesson": next_lesson,
	}
	return render(request, "courses/lesson_detail.html", context)


@login_required
def course_create_view(request: HttpRequest) -> HttpResponse:
	if not request.user.can_author_courses:
		messages.error(request, "Only instructors and admins can create courses.")
		return redirect("courses:list")

	if request.method == "POST":
		form = CourseForm(request.POST)
		if form.is_valid():
			course = form.save(commit=False)
			course.created_by = request.user
			course.save()
			messages.success(request, "Course created successfully. Add lessons from admin.")
			return redirect("courses:detail", slug=course.slug)
	else:
		form = CourseForm()
	return render(request, "courses/course_form.html", {"form": form})


class CourseListApiView(generics.ListAPIView):
	queryset = Course.objects.filter(is_published=True).select_related("created_by")
	serializer_class = CourseSerializer


class CourseDetailApiView(generics.RetrieveAPIView):
	queryset = Course.objects.filter(is_published=True).prefetch_related("lessons")
	serializer_class = CourseSerializer
	lookup_field = "slug"

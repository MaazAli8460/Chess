from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone

from courses.models import Course, Enrollment, LessonProgress
from payments.models import UserSubscription

from .forms import TestimonialForm
from .models import Testimonial


def legal_view(request: HttpRequest, page: str) -> HttpResponse:
	return render(request, f"dashboard/legal_{page}.html")


def home_view(request: HttpRequest) -> HttpResponse:
	featured_courses = Course.objects.filter(is_published=True).order_by("-created_at")[:6]
	testimonials = Testimonial.objects.filter(is_published=True)[:6]
	return render(
		request,
		"dashboard/home.html",
		{
			"featured_courses": featured_courses,
			"testimonials": testimonials,
		},
	)


@login_required
def student_dashboard_view(request: HttpRequest) -> HttpResponse:
	enrollments = list(
		Enrollment.objects.filter(student=request.user)
		.select_related("course")
		.prefetch_related("course__lessons", "lesson_progress")
	)

	total_courses = len(enrollments)
	avg_progress = 0
	if total_courses:
		avg_progress = int(sum(item.completion_percent for item in enrollments) / total_courses)

	# Find next incomplete lesson per enrollment using prefetched data (no extra queries)
	enrollment_data = []
	for enrollment in enrollments:
		completed_ids = {p.lesson_id for p in enrollment.lesson_progress.all() if p.is_completed}
		next_lesson = next(
			(lesson for lesson in enrollment.course.lessons.all() if lesson.id not in completed_ids),
			None,
		)
		enrollment_data.append({"enrollment": enrollment, "next_lesson": next_lesson})

	active_subscription = UserSubscription.objects.filter(
		user=request.user,
		status=UserSubscription.STATUS_ACTIVE,
	).select_related("plan").first()

	# Strength/weakness: learning velocity (lessons completed this week vs last week)
	now = timezone.now()
	week_start = now - timezone.timedelta(days=7)
	prev_week_start = now - timezone.timedelta(days=14)

	lessons_this_week = LessonProgress.objects.filter(
		enrollment__student=request.user,
		is_completed=True,
		completed_at__gte=week_start,
	).count()

	lessons_last_week = LessonProgress.objects.filter(
		enrollment__student=request.user,
		is_completed=True,
		completed_at__gte=prev_week_start,
		completed_at__lt=week_start,
	).count()

	from chesslab.models import AnalysisHistory
	analyses_this_month = AnalysisHistory.objects.filter(
		user=request.user,
		created_at__gte=now - timezone.timedelta(days=30),
	).count()

	velocity_delta = lessons_this_week - lessons_last_week

	return render(
		request,
		"dashboard/student_dashboard.html",
		{
			"enrollment_data": enrollment_data,
			"total_courses": total_courses,
			"avg_progress": avg_progress,
			"active_subscription": active_subscription,
			"lessons_this_week": lessons_this_week,
			"lessons_last_week": lessons_last_week,
			"velocity_delta": velocity_delta,
			"analyses_this_month": analyses_this_month,
		},
	)


@staff_member_required
def testimonial_admin_view(request: HttpRequest) -> HttpResponse:
	if request.method == "POST":
		form = TestimonialForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Testimonial added and ready to display.")
			return redirect("dashboard:testimonial-admin")
	else:
		form = TestimonialForm()

	testimonials = Testimonial.objects.all()
	return render(
		request,
		"dashboard/testimonial_admin.html",
		{
			"form": form,
			"testimonials": testimonials,
		},
	)

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.admin.views.decorators import staff_member_required

from courses.models import Course, Enrollment
from payments.models import UserSubscription

from .forms import TestimonialForm
from .models import Testimonial


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
	enrollments = (
		Enrollment.objects.filter(student=request.user)
		.select_related("course")
		.prefetch_related("course__lessons", "lesson_progress")
	)

	total_courses = enrollments.count()
	avg_progress = 0
	if total_courses:
		avg_progress = int(sum(item.completion_percent for item in enrollments) / total_courses)

	active_subscription = UserSubscription.objects.filter(
		user=request.user,
		status=UserSubscription.STATUS_ACTIVE,
	).select_related("plan").first()

	return render(
		request,
		"dashboard/student_dashboard.html",
		{
			"enrollments": enrollments,
			"total_courses": total_courses,
			"avg_progress": avg_progress,
			"active_subscription": active_subscription,
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

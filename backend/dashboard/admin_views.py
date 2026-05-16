import json
from decimal import Decimal

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.utils import timezone

from courses.models import Course, Enrollment, LessonProgress
from payments.models import PaymentTransaction, UserSubscription
from users.models import User


def _decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


@staff_member_required
def analytics_dashboard(request):
    now = timezone.now()
    twelve_months_ago = now.replace(month=now.month, day=1) if now.month == 12 else \
        now.replace(year=now.year - 1 if now.month <= 1 else now.year,
                    month=(now.month - 1) or 12, day=1)

    revenue_qs = (
        PaymentTransaction.objects
        .filter(status=PaymentTransaction.STATUS_SUCCESS)
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )

    enrollments_qs = (
        Enrollment.objects
        .annotate(month=TruncMonth("enrolled_at"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    top_courses = (
        Course.objects.filter(is_published=True)
        .annotate(
            enrollment_count=Count("enrollments"),
            completed_lessons=Count("enrollments__lesson_progress",
                                    filter=Count("enrollments__lesson_progress__is_completed")),
        )
        .order_by("-enrollment_count")[:10]
    )

    total_revenue = (
        PaymentTransaction.objects
        .filter(status=PaymentTransaction.STATUS_SUCCESS)
        .aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    )
    active_subs = UserSubscription.objects.filter(status=UserSubscription.STATUS_ACTIVE).count()
    total_enrollments = Enrollment.objects.count()
    total_users = User.objects.count()
    total_courses = Course.objects.filter(is_published=True).count()

    revenue_labels = [r["month"].strftime("%b %Y") for r in revenue_qs]
    revenue_data = [float(r["total"]) for r in revenue_qs]
    enrollment_labels = [r["month"].strftime("%b %Y") for r in enrollments_qs]
    enrollment_data = [r["count"] for r in enrollments_qs]

    context = {
        "title": "Analytics Dashboard",
        "total_revenue": total_revenue,
        "active_subs": active_subs,
        "total_enrollments": total_enrollments,
        "total_users": total_users,
        "total_courses": total_courses,
        "top_courses": top_courses,
        "revenue_labels_json": json.dumps(revenue_labels),
        "revenue_data_json": json.dumps(revenue_data),
        "enrollment_labels_json": json.dumps(enrollment_labels),
        "enrollment_data_json": json.dumps(enrollment_data),
    }
    return render(request, "admin/analytics_dashboard.html", context)

from django.urls import path

from .views import home_view, legal_view, student_dashboard_view, testimonial_admin_view

app_name = "dashboard"

urlpatterns = [
    path("", home_view, name="home"),
    path("dashboard/", student_dashboard_view, name="student-dashboard"),
    path("dashboard/testimonials/", testimonial_admin_view, name="testimonial-admin"),
    path("privacy/", legal_view, {"page": "privacy"}, name="privacy"),
    path("terms/", legal_view, {"page": "terms"}, name="terms"),
]

from django.urls import path

from .views import profile_view, resend_verification_view, signup_view, verify_email_view

app_name = "users"

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("profile/", profile_view, name="profile"),
    path("verify/<uidb64>/<token>/", verify_email_view, name="verify-email"),
    path("resend-verification/", resend_verification_view, name="resend-verification"),
]

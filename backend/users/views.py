from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import ProfileForm, SignUpForm
from .tokens import email_verification_token

User = get_user_model()


def _send_verification_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = email_verification_token.make_token(user)
    verify_url = request.build_absolute_uri(f"/users/verify/{uid}/{token}/")

    subject = "Verify your ChessLearn email address"
    text_body = render_to_string(
        "email/verification_email.txt",
        {"user": user, "verify_url": verify_url},
    )
    html_body = render_to_string(
        "email/verification_email.html",
        {"user": user, "verify_url": verify_url},
    )
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        to=[user.email],
    )
    email.attach_alternative(html_body, "text/html")
    email.send(fail_silently=True)


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard:student-dashboard")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.email:
                _send_verification_email(request, user)
                messages.success(
                    request,
                    "Welcome! Check your inbox to verify your email address.",
                )
            else:
                messages.success(request, "Welcome! Your account has been created.")
            return redirect("dashboard:student-dashboard")
    else:
        form = SignUpForm()

    return render(request, "users/signup.html", {"form": form})


def verify_email_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    if user and not user.is_email_verified and email_verification_token.check_token(user, token):
        user.is_email_verified = True
        user.save(update_fields=["is_email_verified"])
        messages.success(request, "Email verified! You now have full access.")
        return render(request, "users/verify_email.html", {"success": True})

    return render(request, "users/verify_email.html", {"success": False})


@login_required
def resend_verification_view(request):
    user = request.user
    if user.is_email_verified:
        messages.info(request, "Your email is already verified.")
        return redirect("dashboard:student-dashboard")
    if not user.email:
        messages.error(request, "Add an email address to your profile first.")
        return redirect("users:profile")
    _send_verification_email(request, user)
    messages.success(request, "Verification email sent. Check your inbox.")
    return redirect("dashboard:student-dashboard")


@login_required
def profile_view(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("users:profile")
    else:
        form = ProfileForm(instance=request.user)

    return render(request, "users/profile.html", {"form": form})

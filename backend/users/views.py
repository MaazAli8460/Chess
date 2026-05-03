from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ProfileForm, SignUpForm


def signup_view(request):
	if request.user.is_authenticated:
		return redirect("dashboard:student-dashboard")

	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Welcome! Your account has been created.")
			return redirect("dashboard:student-dashboard")
	else:
		form = SignUpForm()

	return render(request, "users/signup.html", {"form": form})


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

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
	list_display = ("username", "email", "role", "is_staff", "is_active")
	list_filter = ("role", "is_staff", "is_superuser", "is_active")
	fieldsets = DjangoUserAdmin.fieldsets + (
		(
			"Profile",
			{
				"fields": (
					"role",
					"chess_com_username",
					"bio",
					"is_email_verified",
				)
			},
		),
	)

from django.contrib import admin

from .models import PaymentTransaction, SubscriptionPlan, UserSubscription


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
	list_display = ("name", "price_monthly", "is_active")
	list_filter = ("is_active",)


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
	list_display = ("user", "plan", "status", "starts_at", "ends_at")
	list_filter = ("status", "auto_renew")


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
	list_display = ("user", "amount", "currency", "status", "created_at")
	list_filter = ("status", "currency")

from decimal import Decimal

from django.conf import settings
from django.db import models


class SubscriptionPlan(models.Model):
	name = models.CharField(max_length=120, unique=True)
	description = models.TextField(blank=True)
	price_monthly = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("0.00"))
	stripe_price_id = models.CharField(max_length=255, blank=True)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["price_monthly"]

	def __str__(self) -> str:
		return f"{self.name} (${self.price_monthly}/mo)"


class UserSubscription(models.Model):
	STATUS_ACTIVE = "active"
	STATUS_CANCELED = "canceled"
	STATUS_EXPIRED = "expired"

	STATUS_CHOICES = [
		(STATUS_ACTIVE, "Active"),
		(STATUS_CANCELED, "Canceled"),
		(STATUS_EXPIRED, "Expired"),
	]

	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name="subscriptions",
	)
	plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, related_name="subscriptions")
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
	stripe_subscription_id = models.CharField(max_length=255, blank=True)
	starts_at = models.DateTimeField(auto_now_add=True)
	ends_at = models.DateTimeField(null=True, blank=True)
	auto_renew = models.BooleanField(default=True)

	class Meta:
		ordering = ["-starts_at"]

	def __str__(self) -> str:
		return f"{self.user.username} - {self.plan.name}"


class PaymentTransaction(models.Model):
	STATUS_PENDING = "pending"
	STATUS_SUCCESS = "success"
	STATUS_FAILED = "failed"

	STATUS_CHOICES = [
		(STATUS_PENDING, "Pending"),
		(STATUS_SUCCESS, "Success"),
		(STATUS_FAILED, "Failed"),
	]

	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name="payments",
	)
	amount = models.DecimalField(max_digits=8, decimal_places=2)
	currency = models.CharField(max_length=8, default="USD")
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
	reference = models.CharField(max_length=255, blank=True)
	metadata = models.JSONField(default=dict, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self) -> str:
		return f"{self.user.username} - {self.amount} {self.currency}"

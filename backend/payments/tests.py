from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from users.models import User

from .models import SubscriptionPlan, UserSubscription


class PaymentFlowTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username="payer", password="pass12345")
		self.plan = SubscriptionPlan.objects.create(
			name="Pro",
			price_monthly=Decimal("9.99"),
			is_active=True,
		)

	def test_plans_page_requires_authentication(self):
		response = self.client.get(reverse("payments:plans"))
		self.assertEqual(response.status_code, 302)

	def test_mock_subscription_creates_active_subscription(self):
		self.client.force_login(self.user)
		response = self.client.post(reverse("payments:subscribe-mock", args=[self.plan.id]))
		self.assertEqual(response.status_code, 302)
		self.assertTrue(
			UserSubscription.objects.filter(
				user=self.user,
				status=UserSubscription.STATUS_ACTIVE,
			).exists()
		)

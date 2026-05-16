import json
import logging

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import PaymentTransaction, SubscriptionPlan, UserSubscription

logger = logging.getLogger(__name__)


def _send_payment_confirmation(request_or_none, user, plan, amount) -> None:
	if not user.email:
		return
	base_url = (
		request_or_none.build_absolute_uri("/") if request_or_none else settings.SITE_URL if hasattr(settings, "SITE_URL") else ""
	)
	ctx = {
		"user": user,
		"plan": plan,
		"amount": amount,
		"courses_url": f"{base_url}courses/",
		"dashboard_url": base_url,
	}
	subject = f"Your {plan.name} subscription is active"
	body_txt = render_to_string("email/payment_confirmation.txt", ctx)
	body_html = render_to_string("email/payment_confirmation.html", ctx)
	msg = EmailMultiAlternatives(subject, body_txt, to=[user.email])
	msg.attach_alternative(body_html, "text/html")
	try:
		msg.send()
	except Exception:
		logger.exception("Failed to send payment confirmation to %s", user.email)


def _activate_subscription(user, plan: SubscriptionPlan, reference: str = "mock", request=None) -> None:
	UserSubscription.objects.filter(
		user=user,
		status=UserSubscription.STATUS_ACTIVE,
	).update(status=UserSubscription.STATUS_CANCELED)

	UserSubscription.objects.create(
		user=user,
		plan=plan,
		status=UserSubscription.STATUS_ACTIVE,
		stripe_subscription_id=reference,
	)

	PaymentTransaction.objects.create(
		user=user,
		amount=plan.price_monthly,
		currency="USD",
		status=PaymentTransaction.STATUS_SUCCESS,
		reference=reference,
		metadata={"plan": plan.name},
	)

	_send_payment_confirmation(request, user, plan, plan.price_monthly)


@login_required
def plan_list_view(request: HttpRequest) -> HttpResponse:
	plans = SubscriptionPlan.objects.filter(is_active=True)
	active_subscription = UserSubscription.objects.filter(
		user=request.user,
		status=UserSubscription.STATUS_ACTIVE,
	).select_related("plan").first()
	return render(
		request,
		"payments/plan_list.html",
		{
			"plans": plans,
			"active_subscription": active_subscription,
			"stripe_public_key": settings.STRIPE_PUBLIC_KEY,
		},
	)


@login_required
@require_POST
def subscribe_mock_view(request: HttpRequest, plan_id: int) -> HttpResponse:
	plan = get_object_or_404(SubscriptionPlan, id=plan_id, is_active=True)
	_activate_subscription(request.user, plan, reference="mock-subscription", request=request)
	messages.success(request, f"You are now subscribed to the {plan.name} plan.")
	return redirect("dashboard:student-dashboard")


@login_required
@require_POST
def create_checkout_session_view(request: HttpRequest, plan_id: int) -> HttpResponse:
	plan = get_object_or_404(SubscriptionPlan, id=plan_id, is_active=True)

	if not settings.STRIPE_SECRET_KEY or not plan.stripe_price_id:
		messages.warning(
			request,
			"Stripe is not configured for this plan. Using local mock subscription instead.",
		)
		_activate_subscription(request.user, plan, reference="mock-checkout", request=request)
		return redirect("dashboard:student-dashboard")

	stripe.api_key = settings.STRIPE_SECRET_KEY
	checkout_session = stripe.checkout.Session.create(
		mode="subscription",
		line_items=[{"price": plan.stripe_price_id, "quantity": 1}],
		success_url=request.build_absolute_uri("/payments/success/"),
		cancel_url=request.build_absolute_uri("/payments/plans/"),
		metadata={
			"user_id": request.user.id,
			"plan_id": plan.id,
		},
	)
	return redirect(checkout_session.url)


@login_required
def payment_success_view(request: HttpRequest) -> HttpResponse:
	messages.success(request, "Payment flow completed. Your subscription should be active shortly.")
	return redirect("dashboard:student-dashboard")


@csrf_exempt
def stripe_webhook_view(request: HttpRequest) -> JsonResponse:
	payload = request.body.decode("utf-8")
	sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
	endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

	try:
		if endpoint_secret:
			event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
		else:
			event = json.loads(payload)
	except Exception:
		return JsonResponse({"ok": False}, status=400)

	event_type = event.get("type")
	data_object = event.get("data", {}).get("object", {})

	if event_type == "checkout.session.completed":
		metadata = data_object.get("metadata", {})
		user_id = metadata.get("user_id")
		plan_id = metadata.get("plan_id")
		subscription_id = data_object.get("subscription", "")

		if user_id and plan_id:
			try:
				plan = SubscriptionPlan.objects.get(id=plan_id, is_active=True)
				from users.models import User

				user = User.objects.get(id=user_id)
				_activate_subscription(user, plan, reference=subscription_id or "stripe")
			except (SubscriptionPlan.DoesNotExist, User.DoesNotExist):
				pass

	return JsonResponse({"ok": True})

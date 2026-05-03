from django.urls import path

from .views import (
    create_checkout_session_view,
    payment_success_view,
    plan_list_view,
    stripe_webhook_view,
    subscribe_mock_view,
)

app_name = "payments"

urlpatterns = [
    path("plans/", plan_list_view, name="plans"),
    path("plans/<int:plan_id>/subscribe/", subscribe_mock_view, name="subscribe-mock"),
    path("plans/<int:plan_id>/checkout/", create_checkout_session_view, name="checkout"),
    path("success/", payment_success_view, name="success"),
    path("webhook/stripe/", stripe_webhook_view, name="stripe-webhook"),
]

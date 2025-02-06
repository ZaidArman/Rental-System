from django.urls import path
from .views import CreateCheckoutSession, stripe_webhook, PaymentStatusView

urlpatterns = [
    path('create-checkout-session/', CreateCheckoutSession.as_view(), name="create_checkout_session"),
    path('payment-status/', PaymentStatusView.as_view(), name="payment-status"),
    path('stripe-webhook/', stripe_webhook, name="stripe_webhook"),
]

from django.urls import path
from .views import CreateCheckoutSession, StripeWebhook

urlpatterns = [
    path('create-checkout-session/', CreateCheckoutSession.as_view(), name="create-checkout-session"),
    path('webhook/', StripeWebhook.as_view(), name="stripe-webhook"),
]

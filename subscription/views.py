import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment, SubscriptionPlan
from .serializers import PaymentSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSession(APIView):
    def post(self, request, *args, **kwargs):
        plan_id = request.data.get("plan_id")
        user = request.user

        try:
            plan = SubscriptionPlan.objects.get(id=plan_id)
        except SubscriptionPlan.DoesNotExist:
            return Response({"error": "Plan not found"}, status=status.HTTP_404_NOT_FOUND)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": plan.stripe_price_id,
                    "quantity": 1,
                }
            ],
            mode="subscription",
            success_url="http://localhost:8000/subscription/success/",
            cancel_url="http://localhost:8000/subscription/cancel/",
            customer_email=user.email,
        )

        payment = Payment.objects.create(
            user=user,
            stripe_checkout_id=checkout_session.id,
            status="Pending",
            amount=plan.price,
        )

        return Response({"checkout_url": checkout_session.url})


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhook(APIView):
    def post(self, request, *args, **kwargs):
        payload = request.data
        
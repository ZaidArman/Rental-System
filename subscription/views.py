import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import SubscriptionPlan, Payment
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import RetrieveAPIView
from .serializers import PaymentSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CreateCheckoutSession(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a Stripe checkout session for subscription",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["plan_id"],
            properties={
                "plan_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Subscription Plan ID"),
            },
        ),
        responses={200: openapi.Response("Successful", openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "sessionId": openapi.Schema(type=openapi.TYPE_STRING, description="Stripe Session ID"),
            },
        ))},
    )
    
    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            plan_id = request.data.get("plan_id")
            plan = get_object_or_404(SubscriptionPlan, id=plan_id)

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                customer_email=user.email,
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': plan.name,
                            },
                            'unit_amount': int(plan.price * 100),  # Convert to cents
                            'recurring': {
                                'interval': 'month',  # Change to 'year' for yearly plans
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url="http://127.0.0.1:8000/payment-success/",
                cancel_url="http://127.0.0.1:8000/payment-cancelled/",
            )

            # Save the payment record
            payment = Payment.objects.create(
                user=user,
                stripe_checkout_id=checkout_session.id,
                amount=plan.price,
                status="Pending"
            )

            return Response({'sessionId': checkout_session.id})

        except Exception as e:
            return Response({'error': str(e)}, status=500)


class PaymentStatusView(RetrieveAPIView):
    """
    API endpoint to retrieve user payment status.
    """
    
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)



@swagger_auto_schema(
    method='post',
    operation_description="Stripe webhook for handling payment events",
    responses={200: openapi.Response("Webhook processed successfully")},
)
@api_view(['POST'])  # Add this decorator to make it work with DRF

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers.get("Stripe-Signature", "")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_SECRET_KEY)
    except ValueError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        try:
            payment = Payment.objects.get(stripe_checkout_id=session["id"])
            payment.status = "Paid"
            payment.stripe_payment_intent = session.get("payment_intent")
            payment.save()
        except Payment.DoesNotExist:
            return JsonResponse({'error': 'Payment not found'}, status=404)

    return JsonResponse({'status': 'success'})
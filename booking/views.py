from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Car, Booking, Brand
from .serializers import CarSerializer, BookingSerializer, BrandSerializer
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class BrandsViews(ModelViewSet):
    """
    Viewset for managing car brands.
    """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['brand_name']

    @swagger_auto_schema(
        responses={
            200: openapi.Response('Success', BrandSerializer(many=True))
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CarListView(ModelViewSet):
    """
    Viewset for listing and retrieving cars.
    """
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['status', 'car__car_brand__brand_name', 'car__car_model']

    @swagger_auto_schema(
        responses={
            200: openapi.Response('Success', CarSerializer(many=True))
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class BrandListView(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer



class BookingCreateView(ModelViewSet):
    """
    Viewset for creating and managing bookings.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['status', 'car__car_brand__brand_name', 'car__car_model']

    @swagger_auto_schema(
        request_body=BookingSerializer,
        responses={
            201: openapi.Response('Created', BookingSerializer),
            400: "Bad Request"
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            200: openapi.Response('Success', BookingSerializer(many=True))
        }
    )

    def retrieve(self, request, pk=None):
        """Retrieve a single booking by ID with car details"""
        try:
            booking = self.get_object()
            serializer = self.get_serializer(booking)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    

    def update(self, request, pk=None):
        """Update booking status"""
        from .models import Status
        try:
            booking = self.get_object()
            new_status = request.data.get("status")  # Get status from request

            # Validate status
            if new_status not in dict(Status.choices).keys():
                return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

            # Update only the status field
            booking.status = new_status
            booking.save()

            return Response(
                {"message": "Booking status updated successfully", "status": booking.status},
                status=status.HTTP_200_OK
            )
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
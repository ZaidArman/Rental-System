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

class CarListView(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['status', 'car__car_brand__brand_name', 'car__car_model']


class BrandListView(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer



class BookingCreateView(ModelViewSet):
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
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
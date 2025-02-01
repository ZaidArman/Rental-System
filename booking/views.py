from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Car, Booking
from .serializers import CarSerializer, BookingSerializer


class CarListView(generics.ListAPIView):
    queryset = Car.objects.filter(is_available=True)
    serializer_class = CarSerializer


class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookingUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.user != request.user:
            return Response({"error": "You can only modify your own bookings."}, status=status.HTTP_403_FORBIDDEN)

        if instance.status == 'CONFIRMED':
            return Response({"error": "Confirmed bookings cannot be modified."}, status=status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)


class BookingConfirmView(generics.UpdateAPIView):
    queryset = Booking.objects.filter(status='PENDING')
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.user != request.user:
            return Response({"error": "You can only confirm your own bookings."}, status=status.HTTP_403_FORBIDDEN)

        instance.status = 'CONFIRMED'
        instance.save()

        # Optionally send confirmation email here
        return Response({"message": "Booking confirmed successfully."}, status=status.HTTP_200_OK)

from rest_framework.authtoken.models import Token
from accounts.serializers import SignUpSerializer, LoginSerializer, UserSerializer, ResetPasswordEmail, SetNewPasswordSerializer
from django.utils.timezone import now
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from accounts.models import CustomUser
from accounts.utils import EmailService

class UsersView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated, )

# Sign Up View
class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login View
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'message': 'Login successful!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomForgetPasswordView(APIView):
    serializer_class = ResetPasswordEmail
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email).first()

            if user:
                EmailService().send_email(email, user.user_uuid)
                return Response({"message": "success"}, status=200)
            else:
                return Response({"message": "success"}, status=200)
        else:
            return Response(serializer.errors)
        
class SetNewPasswordView(APIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        current_time = now().timestamp()
        if serializer.is_valid():
            try:
                user = User.objects.filter(user_uuid=serializer.validated_data['uuid']).first()
            except:
                return Response({"message": "token is incorrect"})
            try:
                check_expiry = serializer.validated_data['expiry']
                if float(current_time) > float(check_expiry):
                    return Response({"message": "This link has been expired"}, status=400)
            except:
                pass
            if user:
                new_password = serializer.validated_data['new_password']
                user.set_password(new_password)
                user.is_active = True
                user.save()
                EmailService().password_reset_confirm(user, "Password reset successful")
                return Response({"message": "success", }, status=200)
            return Response({"message": "token not valid", }, status=400)
        else:
            return Response(serializer.errors)
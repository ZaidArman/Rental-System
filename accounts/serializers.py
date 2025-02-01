from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password, CommonPasswordValidator, \
    UserAttributeSimilarityValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    password = serializers.CharField(min_length=8)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'first_name', 'last_name','phone_number']

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        data.pop('password', None)
        data['message'] = "successful"
        return data


# Sign Up Serializer
class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'cnic', 'phone_number', 'address', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            cnic=validated_data['cnic'],
            phone_number=validated_data['phone_number'],
            address=validated_data['address'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user

# Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")
        return user

class ResetPasswordEmail(serializers.Serializer):
    email = serializers.EmailField(required=True)

class SetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, min_length=8)
    uuid = serializers.CharField(required=True)
    expiry = serializers.FloatField(required=False)

    def validate_new_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        if CommonPasswordValidator().validate(value):
            raise serializers.ValidationError('This password is too common.')
        if UserAttributeSimilarityValidator().validate(value):
            raise serializers.ValidationError('This password is too similar to personal information.')
        return value
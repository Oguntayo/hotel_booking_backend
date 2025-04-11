from rest_framework import serializers
from .models import Hotel, Room, Booking
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ModelSerializer, CharField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework_simplejwt.tokens import RefreshToken

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError('Both email and password are required.')

        # Look up the user by email
        self.user = User.objects.filter(email=email).first()
        if not self.user:
            raise serializers.ValidationError('User with this email does not exist.')

        if not self.user.check_password(password):
            raise serializers.ValidationError('Invalid email or password')

        # Generate the refresh and access tokens manually
        refresh = RefreshToken.for_user(self.user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


        
        
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        email = validated_data['email']
        # Ensure the email is unique
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email is already in use.')
        
        password = validated_data['password']
        username = email.split('@')[0]  # auto-generate username from email
        user = User.objects.create_user(username=username, email=email, password=password)
        return user

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        exclude = ['owner'] 

# class RoomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Room
#         fields = '__all__'

class HotelOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']

class GetHotelSerializer(serializers.ModelSerializer):
    owner = HotelOwnerSerializer(read_only=True)

    class Meta:
        model = Hotel
        fields = '__all__'

# class RoomSerializer(serializers.ModelSerializer):
#     hotel = GetHotelSerializer(read_only=True)

#     class Meta:
#         model = Room
# #         fields = '__all__'
# class RoomSerializer(serializers.ModelSerializer):
#     hotel_details = GetHotelSerializer(source='hotel', read_only=True)

#     class Meta:
#         model = Room
#         fields = ['id', 'room_type', 'price_per_hour', 'is_available', 'hotel', 'hotel_details']

class RoomSerializer(serializers.ModelSerializer):
    hotel_details = GetHotelSerializer(source='hotel', read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'room_type', 'price_per_hour', 'is_available', 'hotel', 'hotel_details']
class RoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['room_type', 'price_per_hour', 'is_available', 'hotel']
class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['room', 'guest_name', 'guest_email', 'start_time', 'end_time']
class BookingSerializer(serializers.ModelSerializer):
    room_details = RoomSerializer(source='room', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'guest_name', 'guest_email', 'start_time', 'end_time', 'room', 'room_details']

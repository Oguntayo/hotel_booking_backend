from rest_framework import viewsets
from .models import Hotel, Room, Booking
from .serializers import HotelSerializer, RoomSerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ModelSerializer, CharField
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import EmailTokenObtainPairSerializer,RoomCreateSerializer,BookingCreateSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, EmailTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # Call the original user creation logic
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Now generate JWT tokens for the newly created user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Return the user data along with the tokens
        return Response({
            'user': UserSerializer(user).data,
            'access': access_token,
            'refresh': str(refresh)
        }, status=status.HTTP_201_CREATED)

class EmailLoginView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RoomCreateSerializer
        return RoomSerializer


from rest_framework import viewsets
from .models import Hotel, Room, Booking
from .serializers import HotelSerializer, RoomSerializer, BookingSerializer
from django.conf import settings
import mailtrap as mt  # Import the Mailtrap package

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BookingCreateSerializer
        return BookingSerializer

    def perform_create(self, serializer):
        booking = serializer.save()
        owner_email = booking.room.hotel.owner.email

        # Create the Mailtrap email object
        mail = mt.Mail(
            sender=mt.Address(email="hello@demomailtrap.co", name="Mailtrap Test"),
            to=[mt.Address(email=owner_email)],  # Send email to the hotel owner's email
            subject="New Booking Received",
            text=f"{booking.guest_name} booked {booking.room} from {booking.start_time} to {booking.end_time}.",
            category="Booking Notification",
        )

        # Create the Mailtrap client and send the email
        client = mt.MailtrapClient(token=settings.MAILTRAP_API_TOKEN)  # Ensure the token is set in your settings
        response = client.send(mail)

        # Optionally, log the response for debugging
        print(response)


import mailtrap as mt
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class SendTestEmailView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Create the Mailtrap email object
            mail = mt.Mail(
                sender=mt.Address(email="hello@demomailtrap.co", name="Mailtrap Test"),
                to=[mt.Address(email="oguntayohabeebullah@gmail.com")],  # Replace with the actual recipient email
                subject="You are awesome!",
                text="Congrats for sending test email with Mailtrap!",
                category="Integration Test",
            )

            # Create Mailtrap client with the token
            client = mt.MailtrapClient(token=settings.MAILTRAP_API_TOKEN)

            # Send the email
            response = client.send(mail)

            # Optionally, print the response for debugging
            print(response)

            return Response({"message": "Test email sent successfully!"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

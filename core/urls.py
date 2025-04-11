from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HotelViewSet, RoomViewSet, BookingViewSet,RegisterView,EmailLoginView,SendTestEmailView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import AllBookingsView



router = DefaultRouter()
router.register(r'hotels', HotelViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('send-test-email/', SendTestEmailView.as_view(), name='send_test_email'),
    path('all-bookings/', AllBookingsView.as_view(), name='all_bookings'), 


]
urlpatterns += [
    path('login/', EmailLoginView.as_view(), name='token_obtain_pair'),
]
urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


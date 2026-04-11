from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for ViewSets
router = DefaultRouter()
router.register(r'hotels', views.HotelViewSet, basename='hotel')
router.register(r'room-types', views.RoomTypeViewSet, basename='roomtype')
router.register(r'rooms', views.RoomViewSet, basename='room')
router.register(r'guests', views.GuestViewSet, basename='guest')
router.register(r'bookings', views.BookingViewSet, basename='booking')
router.register(r'payments', views.PaymentViewSet, basename='payment')
router.register(r'services', views.ServiceViewSet, basename='service')
router.register(r'booking-services', views.BookingServiceViewSet, basename='booking-service')
router.register(r'staff', views.StaffViewSet, basename='staff')
router.register(r'reviews', views.ReviewViewSet, basename='review')
router.register(r'maintenance-requests', views.MaintenanceRequestViewSet, basename='maintenance-request')
router.register(r'complaints', views.ComplaintViewSet, basename='complaint')

app_name = 'resultapp'

urlpatterns = [
    path('api/', include(router.urls)),
    # Frontend views
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('booking/', views.BookingView.as_view(), name='booking'),
    path('rooms/', views.RoomsView.as_view(), name='rooms'),
    path('customers/', views.CustomersView.as_view(), name='customers'),
    path('payments/', views.PaymentsView.as_view(), name='payments'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('auth-check/', views.AuthCheckView.as_view(), name='auth-check'),
]

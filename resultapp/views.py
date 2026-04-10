from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import (
    Hotel, RoomType, Room, Guest, Booking, Payment, Staff, Service,
    BookingService, Review, MaintenanceRequest, Complaint
)
from .serializers import (
    HotelSerializer, RoomTypeSerializer, RoomListSerializer, RoomDetailSerializer,
    GuestListSerializer, GuestDetailSerializer, BookingListSerializer,
    BookingDetailSerializer, BookingCreateSerializer, PaymentSerializer,
    ServiceSerializer, BookingServiceSerializer, StaffListSerializer,
    StaffDetailSerializer, ReviewSerializer, MaintenanceRequestSerializer,
    ComplaintSerializer
)


# ============ HOTEL VIEWSET ============

class HotelViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Hotel management.
    - GET /api/hotels/ - List all hotels
    - POST /api/hotels/ - Create new hotel
    - GET /api/hotels/{id}/ - Retrieve specific hotel
    - PUT /api/hotels/{id}/ - Update hotel
    - DELETE /api/hotels/{id}/ - Delete hotel
    """
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'city', 'email']
    ordering_fields = ['created_at', 'name']
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get hotel statistics"""
        hotel = self.get_object()
        total_rooms = hotel.rooms.count()
        available_rooms = hotel.rooms.filter(is_available=True).count()
        total_bookings = hotel.bookings.count()
        revenue = sum([b.total_price for b in hotel.bookings.filter(status='Checked Out')])
        
        return Response({
            'total_rooms': total_rooms,
            'available_rooms': available_rooms,
            'total_bookings': total_bookings,
            'total_revenue': revenue
        })


# ============ ROOM VIEWSETS ============

class RoomTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for Room Types"""
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = [IsAuthenticated]


class RoomViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Room management.
    """
    queryset = Room.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['room_number', 'room_type__name', 'status']
    ordering_fields = ['room_number', 'price_per_night', 'floor']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RoomDetailSerializer
        return RoomListSerializer
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get all available rooms"""
        check_in = request.query_params.get('check_in')
        check_out = request.query_params.get('check_out')
        
        rooms = Room.objects.filter(is_available=True, status='Available')
        
        if check_in and check_out:
            # Filter rooms not booked in the date range
            booked_rooms = Booking.objects.filter(
                Q(check_in_date__lt=check_out) & Q(check_out_date__gt=check_in),
                status__in=['Confirmed', 'Checked In']
            ).values_list('room_id', flat=True)
            rooms = rooms.exclude(id__in=booked_rooms)
        
        serializer = self.get_serializer(rooms, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_maintenance(self, request, pk=None):
        """Mark room as under maintenance"""
        room = self.get_object()
        room.status = 'Maintenance'
        room.is_available = False
        room.save()
        return Response({'status': 'Room marked for maintenance'})


# ============ GUEST VIEWSET ============

class GuestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Guest management.
    """
    queryset = Guest.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    ordering_fields = ['first_name', 'total_bookings', 'created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return GuestDetailSerializer
        return GuestListSerializer
    
    @action(detail=True, methods=['get'])
    def bookings(self, request, pk=None):
        """Get all bookings for a guest"""
        guest = self.get_object()
        bookings = guest.bookings.all()
        serializer = BookingListSerializer(bookings, many=True)
        return Response(serializer.data)


# ============ BOOKING VIEWSET ============

class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Booking management.
    """
    queryset = Booking.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['booking_id', 'guest__first_name', 'guest__last_name']
    ordering_fields = ['check_in_date', 'total_price', 'created_at']
    date_hierarchy = 'check_in_date'
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BookingCreateSerializer
        if self.action == 'retrieve':
            return BookingDetailSerializer
        return BookingListSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new booking with automatic calculations"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        check_in = serializer.validated_data['check_in_date']
        check_out = serializer.validated_data['check_out_date']
        room = serializer.validated_data['room']
        
        # Calculate number of nights and total price
        number_of_nights = (check_out - check_in).days
        total_price = number_of_nights * room.price_per_night
        
        booking = Booking.objects.create(
            number_of_nights=number_of_nights,
            total_price=total_price,
            **serializer.validated_data
        )
        
        # Create payment record
        Payment.objects.create(
            booking=booking,
            amount=total_price,
            payment_method='Online',
            status='Pending'
        )
        
        return Response(
            BookingDetailSerializer(booking).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm a booking"""
        booking = self.get_object()
        booking.status = 'Confirmed'
        booking.save()
        return Response({'status': 'Booking confirmed'})
    
    @action(detail=True, methods=['post'])
    def check_in(self, request, pk=None):
        """Check in a guest"""
        booking = self.get_object()
        booking.status = 'Checked In'
        booking.room.status = 'Occupied'
        booking.save()
        booking.room.save()
        return Response({'status': 'Guest checked in'})
    
    @action(detail=True, methods=['post'])
    def check_out(self, request, pk=None):
        """Check out a guest"""
        booking = self.get_object()
        booking.status = 'Checked Out'
        booking.room.status = 'Available'
        booking.room.is_available = True
        booking.save()
        booking.room.save()
        return Response({'status': 'Guest checked out'})
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a booking"""
        booking = self.get_object()
        booking.status = 'Cancelled'
        booking.room.is_available = True
        booking.save()
        booking.room.save()
        
        # Update payment status
        try:
            payment = booking.payment
            payment.status = 'Refunded'
            payment.save()
        except:
            pass
        
        return Response({'status': 'Booking cancelled'})
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming bookings for today"""
        today = timezone.now().date()
        bookings = Booking.objects.filter(
            check_in_date__gte=today,
            status__in=['Confirmed', 'Pending']
        ).order_by('check_in_date')
        
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)


# ============ PAYMENT VIEWSET ============

class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Payment management.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['booking__booking_id', 'transaction_id', 'payment_method']
    ordering_fields = ['created_at', 'amount', 'status']
    
    @action(detail=True, methods=['post'])
    def process_payment(self, request, pk=None):
        """Process a payment"""
        payment = self.get_object()
        payment.status = 'Completed'
        payment.paid_at = timezone.now()
        payment.save()
        
        # Update booking status
        booking = payment.booking
        if booking.status == 'Pending':
            booking.status = 'Confirmed'
            booking.save()
        
        return Response({
            'status': 'Payment processed',
            'booking_status': booking.status
        })


# ============ SERVICE VIEWSETS ============

class ServiceViewSet(viewsets.ModelViewSet):
    """ViewSet for Services"""
    queryset = Service.objects.filter(is_available=True)
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]


class BookingServiceViewSet(viewsets.ModelViewSet):
    """ViewSet for Booking Services"""
    queryset = BookingService.objects.all()
    serializer_class = BookingServiceSerializer
    permission_classes = [IsAuthenticated]


# ============ STAFF VIEWSET ============

class StaffViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Staff management.
    """
    queryset = Staff.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__first_name', 'user__last_name', 'position']
    ordering_fields = ['hire_date', 'salary', 'position']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return StaffDetailSerializer
        return StaffListSerializer
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active staff"""
        staff = Staff.objects.filter(is_active=True)
        serializer = self.get_serializer(staff, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_position(self, request):
        """Get staff by position"""
        position = request.query_params.get('position')
        if position:
            staff = Staff.objects.filter(position=position)
            serializer = self.get_serializer(staff, many=True)
            return Response(serializer.data)
        return Response({'error': 'Position parameter required'}, status=400)


# ============ REVIEW VIEWSET ============

class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Guest Reviews.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['rating', 'reviewed_at']
    
    @action(detail=False, methods=['get'])
    def average_rating(self, request):
        """Get average ratings"""
        from django.db.models import Avg
        
        reviews = Review.objects.all()
        avg = reviews.aggregate(
            avg_rating=Avg('rating'),
            avg_cleanliness=Avg('cleanliness'),
            avg_service=Avg('service'),
            avg_food=Avg('food')
        )
        return Response(avg)


# ============ MAINTENANCE & COMPLAINT VIEWSETS ============

class MaintenanceRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Maintenance Requests.
    """
    queryset = MaintenanceRequest.objects.all()
    serializer_class = MaintenanceRequestSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['room__room_number', 'priority', 'status']
    ordering_fields = ['created_at', 'priority', 'status']
    
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """Assign maintenance to staff"""
        maintenance = self.get_object()
        staff_id = request.data.get('staff_id')
        
        try:
            staff = Staff.objects.get(id=staff_id)
            maintenance.assigned_to = staff
            maintenance.status = 'In Progress'
            maintenance.save()
            return Response({'status': 'Maintenance assigned'})
        except Staff.DoesNotExist:
            return Response({'error': 'Staff not found'}, status=404)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark maintenance as completed"""
        maintenance = self.get_object()
        maintenance.status = 'Completed'
        maintenance.completed_at = timezone.now()
        maintenance.room.status = 'Available'
        maintenance.room.is_available = True
        maintenance.room.save()
        maintenance.save()
        return Response({'status': 'Maintenance completed'})


class ComplaintViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Guest Complaints.
    """
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['booking__booking_id', 'complaint_type', 'status']
    ordering_fields = ['created_at', 'status']
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Resolve a complaint"""
        complaint = self.get_object()
        complaint.status = 'Resolved'
        complaint.resolution = request.data.get('resolution', '')
        complaint.resolved_at = timezone.now()
        complaint.save()
        return Response({'status': 'Complaint resolved'})

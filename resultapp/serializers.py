from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Hotel, RoomType, Room, Guest, Booking, Payment, Staff, Service,
    BookingService, Review, MaintenanceRequest, Complaint
)


# ============ HOTEL SERIALIZERS ============

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = [
            'id', 'name', 'address', 'city', 'state', 'postal_code',
            'phone', 'email', 'website', 'total_rooms', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


# ============ ROOM SERIALIZERS ============

class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['id', 'name', 'description', 'base_price', 'capacity', 'amenities']


class RoomListSerializer(serializers.ModelSerializer):
    room_type_name = serializers.CharField(source='room_type.name', read_only=True)
    
    class Meta:
        model = Room
        fields = [
            'id', 'room_number', 'room_type', 'room_type_name', 'floor',
            'status', 'price_per_night', 'is_available'
        ]


class RoomDetailSerializer(serializers.ModelSerializer):
    room_type = RoomTypeSerializer(read_only=True)
    
    class Meta:
        model = Room
        fields = [
            'id', 'hotel', 'room_number', 'room_type', 'floor',
            'status', 'price_per_night', 'is_available', 'description',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


# ============ GUEST SERIALIZERS ============

class GuestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone',
            'country', 'total_bookings'
        ]


class GuestDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = [
            'id', 'user', 'first_name', 'last_name', 'email', 'phone',
            'address', 'city', 'country', 'postal_code', 'gender',
            'id_type', 'id_number', 'date_of_birth', 'total_bookings',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'total_bookings']


# ============ BOOKING SERIALIZERS ============

class BookingListSerializer(serializers.ModelSerializer):
    guest_name = serializers.CharField(source='get_guest_name', read_only=True)
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'booking_id', 'guest', 'guest_name', 'room', 'room_number',
            'check_in_date', 'check_out_date', 'status', 'total_price'
        ]


class BookingDetailSerializer(serializers.ModelSerializer):
    guest = GuestDetailSerializer(read_only=True)
    room = RoomDetailSerializer(read_only=True)
    payment = serializers.SerializerMethodField()
    
    class Meta:
        model = Booking
        fields = [
            'id', 'booking_id', 'hotel', 'guest', 'room',
            'check_in_date', 'check_out_date', 'number_of_guests',
            'status', 'number_of_nights', 'total_price', 'notes',
            'payment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['booking_id', 'created_at', 'updated_at', 'number_of_nights']
    
    def get_payment(self, obj):
        try:
            return PaymentSerializer(obj.payment).data
        except:
            return None


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'hotel', 'guest', 'room', 'check_in_date', 'check_out_date',
            'number_of_guests', 'notes'
        ]
    
    def validate(self, data):
        if data['check_out_date'] <= data['check_in_date']:
            raise serializers.ValidationError("Check-out date must be after check-in date.")
        
        room = data['room']
        if not room.is_available:
            raise serializers.ValidationError("This room is not available.")
        
        return data


# ============ PAYMENT SERIALIZERS ============

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id', 'booking', 'amount', 'payment_method', 'status',
            'transaction_id', 'notes', 'paid_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


# ============ SERVICE SERIALIZERS ============

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            'id', 'name', 'service_type', 'description', 'price', 'is_available'
        ]


class BookingServiceSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name', read_only=True)
    
    class Meta:
        model = BookingService
        fields = [
            'id', 'booking', 'service', 'service_name', 'quantity', 'price', 'added_on'
        ]
        read_only_fields = ['added_on', 'price']


# ============ STAFF SERIALIZERS ============

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class StaffListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = Staff
        fields = [
            'id', 'user', 'user_name', 'employee_id', 'position',
            'shift', 'is_active'
        ]


class StaffDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Staff
        fields = [
            'id', 'user', 'employee_id', 'position', 'department',
            'shift', 'phone', 'hire_date', 'salary', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


# ============ REVIEW SERIALIZERS ============

class ReviewSerializer(serializers.ModelSerializer):
    guest_name = serializers.CharField(source='guest.get_full_name', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'booking', 'guest', 'guest_name', 'rating',
            'cleanliness', 'service', 'food', 'comment',
            'would_recommend', 'reviewed_at'
        ]
        read_only_fields = ['reviewed_at']


# ============ MAINTENANCE & COMPLAINT SERIALIZERS ============

class MaintenanceRequestSerializer(serializers.ModelSerializer):
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    assigned_to_name = serializers.CharField(
        source='assigned_to.user.get_full_name', read_only=True
    )
    
    class Meta:
        model = MaintenanceRequest
        fields = [
            'id', 'room', 'room_number', 'priority', 'description',
            'status', 'assigned_to', 'assigned_to_name',
            'created_at', 'completed_at'
        ]
        read_only_fields = ['created_at']


class ComplaintSerializer(serializers.ModelSerializer):
    guest_name = serializers.CharField(source='guest.get_full_name', read_only=True)
    booking_id = serializers.CharField(source='booking.booking_id', read_only=True)
    
    class Meta:
        model = Complaint
        fields = [
            'id', 'booking', 'booking_id', 'guest', 'guest_name',
            'complaint_type', 'description', 'status', 'resolution',
            'created_at', 'resolved_at'
        ]
        read_only_fields = ['created_at']

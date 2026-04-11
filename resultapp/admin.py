from django.contrib import admin
from .models import (
    Hotel, RoomType, Room, Guest, Booking, Payment, Staff, Service,
    BookingService, Review, MaintenanceRequest, Complaint
)

# ============ HOTEL ADMIN ============

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'phone', 'email', 'total_rooms', 'created_at')
    list_filter = ('city', 'created_at')
    search_fields = ('name', 'city', 'email')
    readonly_fields = ('created_at', 'updated_at')


# ============ ROOM MANAGEMENT ADMIN ============

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'base_price')
    search_fields = ('name',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'floor', 'status', 'price_per_night', 'is_available')
    list_filter = ('status', 'room_type', 'floor', 'hotel')
    search_fields = ('room_number', 'room_type__name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Info', {
            'fields': ('hotel', 'room_number', 'room_type', 'floor')
        }),
        ('Pricing & Availability', {
            'fields': ('price_per_night', 'status', 'is_available')
        }),
        ('Details', {
            'fields': ('description',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ============ GUEST ADMIN ============

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'country', 'total_bookings')
    list_filter = ('country', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at', 'total_bookings')
    fieldsets = (
        ('Personal Info', {
            'fields': ('user', 'first_name', 'last_name', 'email', 'phone', 'gender', 'date_of_birth')
        }),
        ('Address', {
            'fields': ('address', 'city', 'country', 'postal_code')
        }),
        ('Identification', {
            'fields': ('id_type', 'id_number')
        }),
        ('Statistics', {
            'fields': ('total_bookings',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ============ BOOKING ADMIN ============

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'guest', 'room', 'check_in_date', 'check_out_date', 'status', 'total_price')
    list_filter = ('status', 'check_in_date', 'hotel')
    search_fields = ('booking_id', 'guest__first_name', 'guest__last_name', 'room__room_number')
    readonly_fields = ('booking_id', 'created_at', 'updated_at', 'number_of_nights')
    date_hierarchy = 'check_in_date'
    fieldsets = (
        ('Booking Info', {
            'fields': ('booking_id', 'hotel', 'guest', 'room')
        }),
        ('Stay Details', {
            'fields': ('check_in_date', 'check_out_date', 'number_of_nights', 'number_of_guests')
        }),
        ('Pricing & Status', {
            'fields': ('status', 'total_price')
        }),
        ('Additional Info', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ============ PAYMENT ADMIN ============

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'payment_method', 'status', 'paid_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('booking__booking_id', 'transaction_id')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Payment Info', {
            'fields': ('booking', 'amount', 'payment_method')
        }),
        ('Status & Transaction', {
            'fields': ('status', 'transaction_id')
        }),
        ('Details', {
            'fields': ('notes', 'paid_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ============ STAFF ADMIN ============

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'position', 'shift', 'is_active', 'hire_date')
    list_filter = ('position', 'shift', 'is_active', 'hire_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'employee_id')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User Account', {
            'fields': ('user',)
        }),
        ('Employment Info', {
            'fields': ('employee_id', 'position', 'department', 'hire_date', 'salary')
        }),
        ('Schedule', {
            'fields': ('shift', 'is_active')
        }),
        ('Contact', {
            'fields': ('phone',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ============ SERVICE ADMIN ============

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type', 'price', 'is_available')
    list_filter = ('service_type', 'is_available')
    search_fields = ('name', 'description')


@admin.register(BookingService)
class BookingServiceAdmin(admin.ModelAdmin):
    list_display = ('booking', 'service', 'quantity', 'price')
    list_filter = ('added_on', 'service__service_type')
    search_fields = ('booking__booking_id', 'service__name')


# ============ REVIEW & RATING ADMIN ============

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('guest', 'rating', 'reviewed_at', 'would_recommend')
    list_filter = ('rating', 'reviewed_at', 'would_recommend')
    search_fields = ('guest__first_name', 'guest__last_name', 'booking__booking_id')
    readonly_fields = ('reviewed_at',)
    fieldsets = (
        ('Review Info', {
            'fields': ('booking', 'guest')
        }),
        ('Ratings', {
            'fields': ('rating', 'cleanliness', 'service', 'food')
        }),
        ('Feedback', {
            'fields': ('comment', 'would_recommend')
        }),
        ('Timestamp', {
            'fields': ('reviewed_at',),
            'classes': ('collapse',)
        }),
    )


# ============ MAINTENANCE & COMPLAINTS ADMIN ============

@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('room', 'priority', 'status', 'created_at', 'completed_at')
    list_filter = ('priority', 'status', 'created_at')
    search_fields = ('room__room_number', 'description')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Room & Priority', {
            'fields': ('room', 'priority')
        }),
        ('Description & Status', {
            'fields': ('description', 'status')
        }),
        ('Assignment', {
            'fields': ('assigned_to',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'completed_at')
        }),
    )


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('booking', 'guest', 'complaint_type', 'status', 'created_at')
    list_filter = ('complaint_type', 'status', 'created_at')
    search_fields = ('booking__booking_id', 'guest__first_name', 'guest__last_name')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Complaint Info', {
            'fields': ('booking', 'guest', 'complaint_type')
        }),
        ('Details', {
            'fields': ('description', 'status')
        }),
        ('Resolution', {
            'fields': ('resolution', 'resolved_at')
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


from .models import Room, Guest, Booking
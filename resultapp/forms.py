from django import forms
from django.contrib.auth.models import User
from .models import (
    Hotel, RoomType, Room, Guest, Booking, Payment, Staff, Service,
    Review, MaintenanceRequest, Complaint
)


# ============ HOTEL FORMS ============

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = [
            'name', 'address', 'city', 'state', 'postal_code',
            'phone', 'email', 'website', 'total_rooms'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'total_rooms': forms.NumberInput(attrs={'class': 'form-control'}),
        }


# ============ ROOM FORMS ============

class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = ['name', 'description', 'base_price', 'capacity', 'amenities']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'base_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'amenities': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            'hotel', 'room_number', 'room_type', 'floor',
            'status', 'price_per_night', 'is_available', 'description'
        ]
        widgets = {
            'hotel': forms.Select(attrs={'class': 'form-control'}),
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
            'room_type': forms.Select(attrs={'class': 'form-control'}),
            'floor': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'price_per_night': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# ============ GUEST FORMS ============

class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = [
            'user', 'first_name', 'last_name', 'email', 'phone',
            'address', 'city', 'country', 'postal_code', 'gender',
            'id_type', 'id_number', 'date_of_birth'
        ]
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'id_type': forms.TextInput(attrs={'class': 'form-control'}),
            'id_number': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


# ============ BOOKING FORMS ============

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'hotel', 'guest', 'room', 'check_in_date', 'check_out_date',
            'number_of_guests', 'notes'
        ]
        widgets = {
            'hotel': forms.Select(attrs={'class': 'form-control'}),
            'guest': forms.Select(attrs={'class': 'form-control'}),
            'room': forms.Select(attrs={'class': 'form-control'}),
            'check_in_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'number_of_guests': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class BookingStatusForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


# ============ PAYMENT FORMS ============

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['booking', 'amount', 'payment_method', 'status', 'transaction_id', 'notes']
        widgets = {
            'booking': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'transaction_id': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


# ============ STAFF FORMS ============

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = [
            'user', 'employee_id', 'position', 'department', 'shift',
            'phone', 'hire_date', 'salary', 'is_active'
        ]
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'shift': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# ============ SERVICE FORMS ============

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'service_type', 'description', 'price', 'is_available']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'service_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# ============ REVIEW FORMS ============

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'booking', 'guest', 'rating', 'cleanliness', 'service',
            'food', 'comment', 'would_recommend'
        ]
        widgets = {
            'booking': forms.Select(attrs={'class': 'form-control'}),
            'guest': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'cleanliness': forms.Select(attrs={'class': 'form-control'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
            'food': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'would_recommend': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# ============ MAINTENANCE & COMPLAINT FORMS ============

class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['room', 'priority', 'description', 'status', 'assigned_to']
        widgets = {
            'room': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
        }


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = [
            'booking', 'guest', 'complaint_type', 'description',
            'status', 'resolution'
        ]
        widgets = {
            'booking': forms.Select(attrs={'class': 'form-control'}),
            'guest': forms.Select(attrs={'class': 'form-control'}),
            'complaint_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'resolution': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

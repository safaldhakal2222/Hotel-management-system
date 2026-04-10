"""
Utility functions for Hotel Management System
"""
from datetime import datetime, date
from decimal import Decimal
from .models import Booking, Room, Payment
from django.db.models import Sum, Avg, Count


# ============ BOOKING UTILITIES ============

def calculate_booking_cost(room, check_in_date, check_out_date):
    """Calculate total booking cost"""
    nights = (check_out_date - check_in_date).days
    if nights <= 0:
        return None
    return nights * room.price_per_night


def get_available_rooms(check_in_date, check_out_date, hotel=None):
    """Get available rooms for the given date range"""
    booked_rooms = Booking.objects.filter(
        check_in_date__lt=check_out_date,
        check_out_date__gt=check_in_date,
        status__in=['Confirmed', 'Checked In']
    ).values_list('room_id', flat=True)
    
    rooms = Room.objects.filter(
        is_available=True,
        status='Available'
    ).exclude(id__in=booked_rooms)
    
    if hotel:
        rooms = rooms.filter(hotel=hotel)
    
    return rooms


def check_room_availability(room, check_in_date, check_out_date):
    """Check if a specific room is available for the given dates"""
    conflicting_bookings = Booking.objects.filter(
        room=room,
        check_in_date__lt=check_out_date,
        check_out_date__gt=check_in_date,
        status__in=['Confirmed', 'Checked In']
    )
    return not conflicting_bookings.exists()


def get_booking_duration(check_in_date, check_out_date):
    """Get the number of nights"""
    return (check_out_date - check_in_date).days


# ============ PAYMENT UTILITIES ============

def generate_transaction_id():
    """Generate a unique transaction ID"""
    import uuid
    return f"TXN-{uuid.uuid4().hex[:12].upper()}"


def get_pending_payments():
    """Get all pending payments"""
    return Payment.objects.filter(status='Pending')


def get_payment_statistics(start_date=None, end_date=None):
    """Get payment statistics"""
    payments = Payment.objects.filter(status='Completed')
    
    if start_date:
        payments = payments.filter(paid_at__gte=start_date)
    if end_date:
        payments = payments.filter(paid_at__lte=end_date)
    
    stats = payments.aggregate(
        total_revenue=Sum('amount'),
        average_payment=Avg('amount'),
        total_transactions=Count('id')
    )
    return stats


# ============ OCCUPANCY UTILITIES ============

def get_occupancy_rate(hotel, start_date=None, end_date=None):
    """Calculate hotel occupancy rate"""
    total_rooms = hotel.rooms.count()
    bookings = hotel.bookings.filter(status__in=['Confirmed', 'Checked In', 'Checked Out'])
    
    if start_date:
        bookings = bookings.filter(check_in_date__gte=start_date)
    if end_date:
        bookings = bookings.filter(check_out_date__lte=end_date)
    
    if total_rooms == 0:
        return 0
    
    occupied_rooms = bookings.values('room').distinct().count()
    occupancy_rate = (occupied_rooms / total_rooms) * 100
    
    return round(occupancy_rate, 2)


def get_total_guests(hotel, start_date=None, end_date=None):
    """Get total number of guests"""
    bookings = hotel.bookings.all()
    
    if start_date:
        bookings = bookings.filter(check_in_date__gte=start_date)
    if end_date:
        bookings = bookings.filter(check_out_date__lte=end_date)
    
    return bookings.aggregate(Total=Sum('number_of_guests'))['Total'] or 0


def get_average_stay(hotel, start_date=None, end_date=None):
    """Get average length of stay"""
    bookings = hotel.bookings.all()
    
    if start_date:
        bookings = bookings.filter(check_in_date__gte=start_date)
    if end_date:
        bookings = bookings.filter(check_out_date__lte=end_date)
    
    avg = bookings.aggregate(Avg=Avg('number_of_nights'))['Avg']
    return round(avg, 2) if avg else 0


# ============ REVENUE UTILITIES ============

def get_revenue(hotel, start_date=None, end_date=None):
    """Get total revenue"""
    bookings = hotel.bookings.filter(status='Checked Out')
    
    if start_date:
        bookings = bookings.filter(check_in_date__gte=start_date)
    if end_date:
        bookings = bookings.filter(check_out_date__lte=end_date)
    
    total = bookings.aggregate(Total=Sum('total_price'))['Total']
    return total or Decimal('0.00')


def get_average_daily_rate(hotel, start_date=None, end_date=None):
    """Calculate Average Daily Rate (ADR)"""
    bookings = hotel.bookings.filter(status__in=['Confirmed', 'Checked In', 'Checked Out'])
    
    if start_date:
        bookings = bookings.filter(check_in_date__gte=start_date)
    if end_date:
        bookings = bookings.filter(check_out_date__lte=end_date)
    
    avg = bookings.aggregate(Avg=Avg('total_price'))['Avg']
    return round(avg, 2) if avg else Decimal('0.00')


def get_revpar(hotel, start_date=None, end_date=None):
    """Calculate Revenue Per Available Room (RevPAR)"""
    revenue = get_revenue(hotel, start_date, end_date)
    total_rooms = hotel.rooms.count()
    
    if total_rooms == 0:
        return Decimal('0.00')
    
    return round(revenue / total_rooms, 2)


# ============ ROOM UTILITIES ============

def get_room_status_distribution(hotel):
    """Get distribution of room statuses"""
    return {
        'Available': hotel.rooms.filter(status='Available').count(),
        'Occupied': hotel.rooms.filter(status='Occupied').count(),
        'Maintenance': hotel.rooms.filter(status='Maintenance').count(),
        'Reserved': hotel.rooms.filter(status='Reserved').count(),
    }


def get_rooms_by_type(hotel):
    """Get room count by type"""
    from django.db.models import Count
    return hotel.rooms.values('room_type__name').annotate(
        count=Count('id')
    ).order_by('room_type__name')


# ============ GUEST UTILITIES ============

def get_guest_statistics(hotel):
    """Get guest statistics"""
    bookings = hotel.bookings.all()
    return {
        'total_guests': get_total_guests(hotel),
        'unique_guests': bookings.values('guest').distinct().count(),
        'total_bookings': bookings.count(),
        'repeat_guests': bookings.values('guest').annotate(
            count=Count('id')
        ).filter(count__gt=1).count(),
    }


# ============ MAINTENANCE UTILITIES ============

def get_maintenance_stats(hotel):
    """Get maintenance request statistics"""
    from .models import MaintenanceRequest
    total_requests = MaintenanceRequest.objects.filter(room__hotel=hotel).count()
    open_requests = MaintenanceRequest.objects.filter(
        room__hotel=hotel,
        status='Open'
    ).count()
    in_progress = MaintenanceRequest.objects.filter(
        room__hotel=hotel,
        status='In Progress'
    ).count()
    
    return {
        'total_requests': total_requests,
        'open': open_requests,
        'in_progress': in_progress,
    }


# ============ COMPLAINT UTILITIES ============

def get_complaint_stats(hotel):
    """Get complaint statistics"""
    from .models import Complaint
    total_complaints = Complaint.objects.filter(booking__hotel=hotel).count()
    open_complaints = Complaint.objects.filter(
        booking__hotel=hotel,
        status='Open'
    ).count()
    resolved_complaints = Complaint.objects.filter(
        booking__hotel=hotel,
        status='Resolved'
    ).count()
    
    return {
        'total_complaints': total_complaints,
        'open': open_complaints,
        'resolved': resolved_complaints,
    }


# ============ REPORT UTILITIES ============

def generate_daily_report(hotel, report_date=None):
    """Generate daily report"""
    if report_date is None:
        report_date = date.today()
    
    bookings = hotel.bookings.filter(
        check_in_date__lte=report_date,
        check_out_date__gt=report_date,
        status__in=['Confirmed', 'Checked In']
    )
    
    check_ins = hotel.bookings.filter(
        check_in_date=report_date,
        status='Confirmed'
    )
    
    check_outs = hotel.bookings.filter(
        check_out_date=report_date,
        status='Checked In'
    )
    
    return {
        'date': report_date,
        'occupied_rooms': bookings.values('room').distinct().count(),
        'total_guests': bookings.aggregate(Total=Sum('number_of_guests'))['Total'] or 0,
        'check_ins': check_ins.count(),
        'check_outs': check_outs.count(),
        'available_rooms': hotel.rooms.filter(is_available=True).count(),
    }


def generate_monthly_report(hotel, year, month):
    """Generate monthly report"""
    from datetime import datetime
    start_date = date(year, month, 1)
    
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)
    
    bookings = hotel.bookings.filter(
        check_in_date__gte=start_date,
        check_in_date__lt=end_date,
        status__in=['Confirmed', 'Checked In', 'Checked Out']
    )
    
    return {
        'year': year,
        'month': month,
        'total_bookings': bookings.count(),
        'total_guests': bookings.aggregate(Total=Sum('number_of_guests'))['Total'] or 0,
        'total_revenue': bookings.aggregate(Total=Sum('total_price'))['Total'] or Decimal('0.00'),
        'average_stay': bookings.aggregate(Avg=Avg('number_of_nights'))['Avg'] or 0,
        'occupancy_rate': get_occupancy_rate(hotel, start_date, end_date),
    }

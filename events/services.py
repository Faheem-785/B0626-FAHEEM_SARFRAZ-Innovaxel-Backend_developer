from django.db import transaction
from django.db.models import F
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Event, Registration


class EventService:

    @staticmethod
    def create_event(name, total_seats, event_date):
        if total_seats <= 0:
            raise ValueError("Total seats must be greater than 0")

        if Event.objects.filter(name=name).exists():
            raise ValueError("Event name must be unique")

        event = Event.objects.create(
            name=name,
            total_seats=total_seats,
            event_date=event_date
        )
        return event


class RegistrationService:

    @staticmethod
    def register_user(user_name, event_id):
        with transaction.atomic():
            # Safely lock the event row to prevent race conditions
            event = Event.objects.select_for_update().filter(id=event_id).first()

            if not event:
                raise ValueError("Event not found")

            # Look up any existing registration (ACTIVE or CANCELLED)
            existing_reg = Registration.objects.filter(
                user_name=user_name, 
                event=event
            ).first()
            
            if existing_reg:
                if existing_reg.status == 'ACTIVE':
                    raise ValueError("You are already registered for this event!")
                
                elif existing_reg.status == 'CANCELLED':
                    # ❌ Double-booking guard check before updating the seat
                    if event.active_registrations.count() >= event.total_seats:
                        raise ValueError("Event is full")
                    
                    # ✅ Reactivate the entry safely
                    existing_reg.status = 'ACTIVE'
                    existing_reg.save()
                    return existing_reg

            # If no record exists at all, make a brand new one
            if event.active_registrations.count() >= event.total_seats:
                raise ValueError("Event is full")
                
            registration = Registration.objects.create(
                user_name=user_name,
                event=event,
                status='ACTIVE',
                created_at=timezone.now()
            )
            return registration

    @staticmethod
    def cancel_registration(user_name, event_id):
        registration = Registration.objects.filter(
            user_name=user_name,
            event_id=event_id,
            status='ACTIVE'
        ).first()

        if not registration:
            raise ValueError("Active registration not found")

        registration.status = 'CANCELLED'
        registration.save()
        return registration
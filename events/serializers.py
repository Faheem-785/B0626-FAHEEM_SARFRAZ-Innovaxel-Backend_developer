from rest_framework import serializers
from django.utils.timezone import now

from .models import (
    Event,
    Registration
)


class EventSerializer(
    serializers.ModelSerializer
):

    available_seats = (
        serializers.ReadOnlyField()
    )

    total_registrations = (
        serializers.SerializerMethodField()
    )

    class Meta:
        model = Event

        fields = [
            'id',
            'name',
            'total_seats',
            'event_date',
            'available_seats',
            'total_registrations'
        ]

    def get_total_registrations(
        self,
        obj
    ):
        return (
            obj.active_registrations
        )

    def validate_event_date(
        self,
        value
    ):
        if value <= now():
            raise serializers.ValidationError(
                "Event date "
                "must be future."
            )

        return value


class RegistrationSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Registration

        fields = [
            'id',
            'user_name',
            'event',
            'status',
            'registered_at'
        ]

        read_only_fields = [
            'status',
            'registered_at'
        ]
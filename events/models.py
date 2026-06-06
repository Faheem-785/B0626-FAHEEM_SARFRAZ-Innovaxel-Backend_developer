from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class Event(models.Model):

    name = models.CharField(
        max_length=255,
        unique=True
    )

    total_seats = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    event_date = models.DateTimeField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['event_date']

    @property
    def active_registrations(self):
        return self.registrations.filter(status='ACTIVE')

    @property
    def available_seats(self):
        return self.total_seats - self.active_registrations.count()
    
    @property
    def total_registrations(self):
        return self.registrations.count()

    def __str__(self):
        return self.name


class Registration(models.Model):
    user_name = models.CharField(max_length=100)
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='registrations'  # ⭐ IMPORTANT FIX
    )
    status = models.CharField(max_length=20, default='ACTIVE')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user_name', 'event')
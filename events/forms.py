from django import forms
from django.utils.timezone import now
from .models import Event


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['name', 'total_seats', 'event_date']

        widgets = {
            # Text input
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Event Name'
            }),

            # Number input
            'total_seats': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Total Seats'
            }),

            # ⭐ THIS IS THE IMPORTANT PART (Calendar + Time Picker)
            'event_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control form-control-lg'
                }
            ),
        }

    def clean_total_seats(self):
        seats = self.cleaned_data['total_seats']
        if seats <= 0:
            raise forms.ValidationError("Total seats must be greater than 0")
        return seats

    def clean_event_date(self):
        event_date = self.cleaned_data['event_date']

        if event_date <= now():
            raise forms.ValidationError("Event date must be in the future")

        return event_date
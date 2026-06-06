from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.db import IntegrityError
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Event, Registration
from .serializers import EventSerializer, RegistrationSerializer
from .forms import EventForm
from .services import EventService, RegistrationService
from .utils import success_response, error_response


# -----------------------
# TEMPLATE VIEWS
# -----------------------

def home_page(request):
    return render(request, 'events/home.html')


def create_event_page(request):
    message = None

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            message = "Event created successfully!"
            form = EventForm()  # reset form
        else:
            message = "Please fix the errors below."
    else:
        form = EventForm()

    return render(request, 'events/create_event.html', {
        "form": form,
        "message": message
    })


def events_page(request):
    card_error = None
    error_event_id = None

    if request.method == 'POST':
        action = request.POST.get('action')
        raw_event_id = request.POST.get('event_id')
        user_name = request.POST.get('user_name')

        try:
            if raw_event_id:
                error_event_id = int(raw_event_id)
        except (ValueError, TypeError):
            error_event_id = None

        try:
            # ---------------- CANCEL ----------------
            if action == "cancel":
                RegistrationService.cancel_registration(
                    user_name=user_name,
                    event_id=raw_event_id
                )
                messages.success(request, "Registration cancelled successfully!")
                error_event_id = None

            # ---------------- REGISTER ----------------
            else:
                RegistrationService.register_user(
                    user_name=user_name,
                    event_id=raw_event_id
                )
                messages.success(request, "Successfully registered!")
                error_event_id = None

        except Exception as e:
            card_error = str(e)

    # Base query instantiated first
    events = Event.objects.all()

    # 🔥 FILTER: upcoming only
    if request.GET.get("upcoming") == "true":
        events = events.filter(event_date__gt=now())

    # 🔥 SORTING
    sort = request.GET.get("sort")
    if sort == "date":
        events = events.order_by("event_date")
    elif sort == "name":
        events = events.order_by("name")

    return render(request, 'events/event_list.html', {
        'events': events,
        'card_error': card_error,
        'error_event_id': error_event_id
    })


# -----------------------
# EVENT APIs
# -----------------------

class EventCreateAPIView(APIView):
    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class EventListAPIView(APIView):
    def get(self, request):
        queryset = Event.objects.all()
        if request.query_params.get('upcoming') == 'true':
            queryset = queryset.filter(event_date__gt=now())
        queryset = queryset.order_by('event_date')
        return Response(EventSerializer(queryset, many=True).data)


# -----------------------
# REGISTRATION API
# -----------------------

class RegisterAPIView(APIView):
    def post(self, request):
        try:
            registration = RegistrationService.register_user(
                user_name=request.data.get('user_name'),
                event_id=request.data.get('event_id')
            )
            return Response(
                RegistrationSerializer(registration).data,
                status=201
            )
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class CancelRegistrationAPIView(APIView):
    def post(self, request):
        registration = Registration.objects.filter(
            user_name=request.data.get('user_name'),
            event_id=request.data.get('event_id'),
            status='ACTIVE'
        ).first()

        if not registration:
            return Response(
                {"error": "Registration not found."},
                status=404
            )

        registration.status = 'CANCELLED'
        registration.save()
        return Response({"message": "Registration cancelled."})


# -----------------------
# SERVICE-BASED APIs (CLEAN)
# -----------------------

class CreateEventAPI(APIView):
    def post(self, request):
        try:
            event = EventService.create_event(
                name=request.data.get("name"),
                total_seats=int(request.data.get("total_seats") or 0),
                event_date=request.data.get("event_date")
            )
            return Response(
                success_response(
                    "Event created successfully",
                    EventSerializer(event).data
                ),
                status=201
            )
        except ValueError as e:
            return Response(error_response(str(e)), status=400)


class EventListAPI(APIView):
    def get(self, request):
        events = Event.objects.all()
        if request.GET.get("upcoming") == "true":
            events = events.filter(event_date__gt=now())
        events = events.order_by("event_date")
        return Response(
            success_response(
                "Events fetched successfully",
                EventSerializer(events, many=True).data
            )
        )


class RegisterAPI(APIView):
    def post(self, request):
        try:
            registration = RegistrationService.register_user(
                user_name=request.data.get("user_name"),
                event_id=request.data.get("event_id")
            )
            return Response(
                success_response(
                    "User registered successfully",
                    RegistrationSerializer(registration).data
                ),
                status=201
            )
        except Exception as e:
            return Response(error_response(str(e)), status=400)


class CancelAPI(APIView):
    def post(self, request):
        try:
            registration = RegistrationService.cancel_registration(
                user_name=request.data.get("user_name"),
                event_id=request.data.get("event_id")
            )
            return Response(
                success_response(
                    "Registration cancelled successfully",
                    RegistrationSerializer(registration).data
                )
            )
        except Exception as e:
            return Response(error_response(str(e)), status=400)
from django.urls import path
from .views import (
    home_page,
    create_event_page,
    events_page,
    CreateEventAPI,
    EventListAPI,
    RegisterAPI,
    CancelAPI,
)

urlpatterns = [
    # --------------------
    # HTML Pages
    # --------------------
    path('', home_page, name='home'),
    path('create-event-page/', create_event_page, name='create_event'),
    path('events-page/', events_page, name='events_page'),

    # --------------------
    # API Endpoints
    # --------------------
    path('events/create/', CreateEventAPI.as_view(), name='api_create_event'),
    path('events/', EventListAPI.as_view(), name='api_event_list'),
    path('register/', RegisterAPI.as_view(), name='api_register'),
    path('cancel/', CancelAPI.as_view(), name='api_cancel'),
]
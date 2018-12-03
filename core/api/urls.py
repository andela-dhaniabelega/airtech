from django.urls import path

from core.api import views

urlpatterns = [
    path('flights/', views.FlightList.as_view()),
    path('flights/<int:pk>/', views.FlightDetails.as_view()),
    path('flights/<int:pk>/status/', views.check_flight_status),
    path('flights/reservations/', views.check_flight_reservations),
    path('tickets/', views.TicketList.as_view()),
    path('tickets/<int:pk>/', views.TicketDetails.as_view()),
    path('user/login/', views.UserLogin.as_view()),
    path('user/create/', views.UserCreate.as_view()),
    path('user/<int:pk>/upload_photo/', views.PhotoUpdateDestroy.as_view()),
]

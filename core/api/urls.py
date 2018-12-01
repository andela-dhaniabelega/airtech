from django.urls import path

from core.api import views

urlpatterns = [
    path('flights/', views.FlightList.as_view()),
    path('flights/<int:flight_id>/', views.FlightDetails.as_view()),
    path('flights/<int:flight_id>/status', views.check_flight_status),
    path('flights/reservations', views.check_flight_reservations),
    path('tickets/purchase', views.TicketList.as_view()),
    path('tickets/<int:flight_id>', views.TicketDetails.as_view()),
    path('user/login', views.UserLogin.as_view()),
    path('user/create', views.UserCreate.as_view()),
    path('user/<int:user_id>/upload_photo', views.PhotoUpdateDestroy.as_view()),
]

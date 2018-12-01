from django.urls import path

from core.api import views

urlpatterns = [
    path('flights/', views.FlightList.as_view()),
    path('flights/<int:flight_id>/', views.FlightDetails.as_view()),
    # path('flight/<int:flight_id>/check_status', views.index, name='index'),
    # path('flight/<int:flight_id>/check_reservations', views.index, name='index'),
    path('tickets/purchase', views.TicketPurchaseList.as_view()),
    # path('ticket/<int:flight_id>/reserve', views.index, name='index'),
    path('user/login', views.UserLogin.as_view()),
    path('user/create', views.UserCreate.as_view()),
    path('user/<int:user_id>/upload_photo', views.PhotoUpdateDestroy.as_view()),
]

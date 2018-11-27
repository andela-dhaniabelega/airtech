from django.urls import path

from . import views

urlpatterns = [
    path('flight/create', views.index, name='index'),
    path('flight/<int:flight_id>/update', views.index, name='index'),
    path('flight/<int:flight_id>/check_status', views.index, name='index'),
    path('flight/<int:flight_id>/check_reservations', views.index, name='index'),
    path('ticket/<int:flight_id>/purchase', views.index, name='index'),
    path('ticket/<int:flight_id>/reserve', views.index, name='index'),
    path('user/login', views.index, name='index'),
    path('user/create', views.index, name='index'),
    path('user/<int:user_id>/upload_photo', views.index, name='index'),
]

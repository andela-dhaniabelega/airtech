from django.urls import path

from core.api import views

urlpatterns = [
    # path('flight/create', views.index, name='index'),
    # path('flight/<int:flight_id>/update', views.index, name='index'),
    # path('flight/<int:flight_id>/check_status', views.index, name='index'),
    # path('flight/<int:flight_id>/check_reservations', views.index, name='index'),
    # path('ticket/<int:flight_id>/purchase', views.index, name='index'),
    # path('ticket/<int:flight_id>/reserve', views.index, name='index'),
    path('user/login', views.UserLogin.as_view()),
    path('user/create', views.UserCreate.as_view()),
    # path('user/<int:user_id>/upload_photo', views.index, name='index'),
]
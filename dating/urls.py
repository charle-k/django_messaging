from django.urls import path
from . import views


app_name = 'dating'
urlpatterns = [
    path('', views.home, name='home'),
    path('me/', views.dashboard_user, name='dashboard_user'),
    path('my_friends/', views.my_friends, name='my_friends'),

    ]

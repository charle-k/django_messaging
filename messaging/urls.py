from django.urls import path
from . import views


app_name = 'messaging'
urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('inbox/chat/<int:profile_number>/', views.chat, name='chat'),
    path('inbox/chat/<int:profile_number>/send_message', views.send_message, name='send_message'),
    path('inbox/chat/<int:profile_number>/edit/<int:message_id>/', views.edit, name = 'message_edit')
    # path('inbox/chat/<int:profile_number>/edit/<int:pk>/delete/<int:pk>/', views.delete, name='message_delete')

]

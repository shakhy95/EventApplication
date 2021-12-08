from django.urls import path
from . import views
# import class LoginView for login authentication
# https://docs.djangoproject.com/en/2.1/topics/auth/default/#django.contrib.auth.views.LoginView
#from django.contrib.auth.views import LoginView


urlpatterns = [
    # /matchings/
    path('', views.home, name='home'),
    # /matchings/login
    path('login/', views.login, name='login'),
    # /matchings/logout
    path('logout/', views.logout, name='logout'),
    # /matchings/signup
    path('signup/', views.signup, name='signup'),
    # /matchings/register
    path('register/', views.register, name='register'),
    # /matchings/profile
    path('profile/', views.profile, name='profile'),
    # /matchings/edit_profile
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    # Ajax: upload new profile picture
    path('upload_image/', views.upload_image, name='uploadi_mage'),
    # /matchings/hobby_matching
    path('hobby_matching/', views.hobby_matching, name='hobby_matching'),
    # /matchings/message_send
    path('message_send/', views.message_send, name='message_send'),
    # /matchings/message_inbox
    path('message_inbox/', views.message_inbox, name='message_inbox'),
    # /matchings/message_outbox
    path('message_outbox/', views.message_outbox, name='message_outbox'),
    # /matchings/event_create
    path('event_create/', views.event_create, name='event_create'),
    # /matchings/events_public
    path('event_public/', views.events_public, name='events_public'),
    # /matchings/events_private
    path('event_private/', views.events_private, name='events_private'),
    # Ajax : join evnt
    path('join_event/', views.join_event, name='join_event'),
]

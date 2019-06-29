from django.urls import path, include
from . import views

# url - 'profiles/'
urlpatterns = [
    path('search', views.search, name='search'),
    path('<int:profile_id>', views.profile, name='profile'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('notifications', views.notifications, name='notifications'),
    path('request_sent', views.requests, name='requests'),
    path('request_received', views.requests_recv, name='request_recv'),
    path('messages', views.message, name='messages'),
    path('myprojects', views.myProjects, name='my_project'),
]
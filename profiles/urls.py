from django.urls import path, include
from . import views

# url - 'profile/'
urlpatterns = [
    path('search', views.search, name='search'),
    path('<int:profile_id>', views.profile, name='profile'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('dashboard', views.dashboard, name='dashboard'),
]
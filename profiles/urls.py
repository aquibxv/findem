from django.urls import path
from . import views

# url - 'profile/'
urlpatterns = [
    path('search', views.search, name='search'),
    path('<int:profile_id>', views.profile, name='profile'),
]
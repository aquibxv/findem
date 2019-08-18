from django.urls import path
# from django.contrib.auth.views import password_reset, password_reset_done
from . import views
from django.contrib.auth import views as auth_views

# url pattern = '/
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('home', views.home, name='home'),
    path('feedback', views.feedback, name='feedback'),
    path('forgot_password', views.forgotPassword, name="reset_password"),
]
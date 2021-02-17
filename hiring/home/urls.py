from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from .views import HomeView

urlpatterns = [
    path('', HomeView.as_view()),
    path('log_cabin_challenge/', HomeView.as_view()),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('sign_up/', TemplateView.as_view(template_name="sign_up.html"), name="signup"),
]
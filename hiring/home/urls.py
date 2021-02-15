from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', TemplateView.as_view(template_name="home.html")),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('sign_up/', TemplateView.as_view(template_name="sign_up.html"), name="signup"),
]
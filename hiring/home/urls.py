from django.urls import path

from .views import HomeView, ChallengeDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('challenge/<slug:slug>/', ChallengeDetailView.as_view(), name='challenge_detail'),
]
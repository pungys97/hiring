from django.urls import path

from .views import HomeView, ChallengeDetailView, ScoreboardView, ContactView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('scoreboard/', ScoreboardView.as_view(), name='scoreboard'),
    path('contact_us/', ContactView.as_view(), name='contact'),
    path('challenge/<slug:slug>/', ChallengeDetailView.as_view(), name='challenge_detail'),
]
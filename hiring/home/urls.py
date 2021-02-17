from django.urls import path

from .views import HomeView, ChallengeView

urlpatterns = [
    path('', HomeView.as_view()),
    path('challenge/<slug:slug>/', ChallengeView.as_view(), name='challenge_detail'),
]
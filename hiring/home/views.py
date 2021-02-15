from django.shortcuts import render
from django.views.generic import ListView
from .models import Challenge


class ChallengeView(ListView):
    model = Challenge

    def get(self, request, *args, **kwargs):
        challenges = Challenge.objects.filter(is_published=True).order_by('created_date_time')
        return render(request, template_name='home.html', context={"challenges" : challenges})

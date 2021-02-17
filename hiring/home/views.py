from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Challenge


class ChallengeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['challenges'] = Challenge.objects.filter(is_published=True).order_by('created_date_time')[:6]
        return context


# CHALLENGES
class LogCabinView(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        challenges = Challenge.objects.filter(is_published=True).order_by('created_date_time')
        return render(request, template_name='home.html', context={"challenges": challenges})

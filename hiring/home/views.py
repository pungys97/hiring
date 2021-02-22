from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import FormMixin

from .forms import ChallengeForm
from .models import Challenge


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['challenges'] = Challenge.objects.filter(is_published=True).order_by('created_date_time')[:6]
        return context


class ChallengeView(FormMixin, DetailView):
    template_name = 'solutions/base_solution_template.html'
    model = Challenge
    form_class = ChallengeForm

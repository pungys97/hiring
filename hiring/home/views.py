import importlib

from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView

from .fields import Field
from .forms import ChallengeForm
from .models import Challenge
from .utils import get_logger

logger = get_logger(__name__)


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['challenges'] = Challenge.objects.filter(is_published=True).order_by('created_date_time')[:6]  #TODO: pagination for challenges
        return context


class ChallengeDisplayView(DetailView):
    template_name = 'solutions/solution_template.html'
    model = Challenge

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ChallengeForm(
            fields=
            (
                Field(name='x', value='7', field_type=Field.INPUT),
                Field(name='y', value='8', field_type=Field.INPUT),
                Field(name='z', value='8', field_type=Field.INPUT),
                Field(name='solution', field_type=Field.SOLUTION),
            )
        )
        return context


class ChallengeAnswerView(SingleObjectMixin, FormView):
    form_class = ChallengeForm
    model = Challenge

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        solver = importlib.import_module(self.object.solver_script_path, package='home')
        logger.debug("true")
        res = solver.Solver(11, 10) == form.data['solution']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('home')


class ChallengeDetailView(View):

    def get(self, request, *args, **kwargs):
        view = ChallengeDisplayView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ChallengeAnswerView.as_view()
        return view(request, *args, **kwargs)

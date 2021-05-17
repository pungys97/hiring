import importlib
from collections import defaultdict
from datetime import datetime

from django.core.signing import Signer
from django.db.models import Max
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.views import View
from django.views.generic import TemplateView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView
from random_username.generate import generate_username

from .fields import Field
from .forms import ChallengeForm
from .models import Challenge, ChallengeAttempt
from .utils import get_logger, verify_timestamp

logger = get_logger(__name__)


def get_username(request):
    username = request.COOKIES.get('username', generate_username()[0])
    return username


class HomeView(TemplateView):
    template_name = 'home.html'

    @cached_property
    def username(self):
        return get_username(self.request)

    @cached_property
    def scores(self):
        max_scores = ChallengeAttempt.objects.all().values('challenge').annotate(max_score=Max('score'))
        max_scores = {challenge['challenge']: challenge['max_score'] for challenge in max_scores}
        scores = ChallengeAttempt.objects.all().values('attempted_by', 'challenge').annotate(score=Max('score')).order_by('attempted_by')
        data = defaultdict(list)
        for score in scores:
            score['score_norm'] = score['score'] / max_scores[score['challenge']]
            user = score.pop('attempted_by')
            data[user].append(score)
        sorted_data = sorted(
            data.items(),
            key=lambda x: sum(y['score_norm'] for y in x[1]),
            reverse=True
        )
        print(sorted_data)
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['challenges'] = Challenge.objects.filter(is_published=True).order_by('created_date_time')[:6]  # TODO: pagination for challenges
        context['username'] = self.username
        context['scores'] = self.scores
        return context

    def get(self, request, *args, **kwargs):
        res = super().get(request, *args, **kwargs)
        res.set_cookie('username', self.username)
        return res


class ChallengeDisplayView(DetailView):
    template_name = 'solutions/solution_template.html'
    model = Challenge
    signer = Signer()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ChallengeForm(
            fields=
            (
                Field(name='width', value='11', field_type=Field.INPUT),
                Field(name='height', value='10', field_type=Field.INPUT),
                Field(name='solution', field_type=Field.SOLUTION),
            ),
            initial={'timestamp': ChallengeDisplayView.signer.sign(timezone.now().isoformat())}
        )
        return context


class ChallengeAnswerView(SingleObjectMixin, FormView):
    form_class = ChallengeForm
    model = Challenge

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def save_solution_attempt(self, data):
        username = get_username(self.request)
        logger.debug(f"username = {username}")
        solver_module = importlib.import_module(self.object.solver_script_path, package='home')
        timestamp = verify_timestamp(data.get('timestamp', ''))
        if timestamp:
            duration = timezone.now() - datetime.fromisoformat(timestamp)
        else:
            return
        logger.debug(f"started - {timestamp}, finished - {timezone.now()}")
        logger.debug(f"Solution took {duration}.")
        solver = solver_module.Solver(**data)
        attempt = ChallengeAttempt(
            challenge=self.object,
            attempted_by=username,
            attempted_date_time=timestamp,
            score=solver.get_score(),
            duration=duration,
            completed=solver.solve(data['solution'])
        )
        attempt.save()

    def form_valid(self, form):
        self.save_solution_attempt(form.data)
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

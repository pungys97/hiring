import importlib
from collections import defaultdict
from datetime import datetime

from django.core.cache import cache
from django.core.paginator import Paginator
from django.core.signing import Signer
from django.db.models import Max
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.views import View
from django.views.generic import TemplateView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView
from random_username.generate import generate_username

from .forms import ChallengeForm, ContactForm
from .models import Challenge, ChallengeAttempt
from .utils import get_logger, verify_signature

logger = get_logger(__name__)

CACHE_SCORES_KEY = 'scores_cache'
CACHE_SCORES_KEY_VALID_FOR = 10 * 60  # cache for 10 mins


def get_username(request):
    username = request.COOKIES.get('username', generate_username()[0])
    return username


def published_challenges():
    return Challenge.objects.filter(is_published=True).order_by('created_date_time')


def compute_scores():
    published_challenges_ = tuple(published_challenges().values_list('id', flat=True))
    published_challenges_attempts = ChallengeAttempt.objects.filter(challenge__is_published=True)
    max_scores = published_challenges_attempts.values('challenge').annotate(max_score=Max('score'))
    max_scores = {challenge['challenge']: challenge['max_score'] for challenge in max_scores}
    scores = published_challenges_attempts.values('attempted_by', 'challenge').annotate(
        score=Max('score')
    ).order_by('attempted_by')  # TODO: show time instead of score
    data = defaultdict(lambda: [None for _ in range(
        len(published_challenges_))])  # create initial list of length no. of published challenges == column count
    for score in scores:
        score['score_norm'] = score['score'] / max_scores[score['challenge']]
        user = score.pop('attempted_by')
        column_idx = published_challenges_.index(
            score['challenge'])  # used to assign proper column in scoreboard table
        data[user][column_idx] = score
    sorted_data = sorted(
        data.items(),
        key=lambda x: sum(y['score_norm'] if y else 0 for y in x[1]),
        reverse=True
    )
    cache.set(CACHE_SCORES_KEY, sorted_data, )
    return sorted_data


class HomeView(TemplateView):
    template_name = 'home.html'

    @cached_property
    def username(self):
        return get_username(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_5'] = cache.get(CACHE_SCORES_KEY, compute_scores())[:5]  # get top 5
        context['challenges'] = published_challenges()
        context['username'] = self.username
        return context

    def get(self, request, *args, **kwargs):
        res = super().get(request, *args, **kwargs)
        res.set_cookie('username', self.username)
        return res


class ScoreboardView(TemplateView):
    template_name = 'scoreboard.html'

    @cached_property
    def username(self):
        return get_username(self.request)

    def get_context_data(self, **kwargs):
        scores = cache.get(CACHE_SCORES_KEY, compute_scores())
        paginator = Paginator(scores, 2)
        page_number = int(self.request.GET.get('page', '1'))
        page_obj = paginator.get_page(page_number)

        context = super().get_context_data(**kwargs)
        context['username'] = self.username
        context['challenges'] = published_challenges()
        context['page_obj'] = page_obj
        context['page_two_plus'] = paginator.num_pages > 1
        return context

    def get(self, request, *args, **kwargs):
        res = super().get(request, *args, **kwargs)
        res.set_cookie('username', self.username)
        return res


class ChallengeDisplayView(DetailView):
    SIGNATURE_MESSAGE = "%s;%s"
    template_name = 'solutions/solution_template.html'
    model = Challenge
    signer = Signer()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        generator_module = importlib.import_module(self.object.generator_script_path, package='home')
        fields, seed = generator_module.Generator().generate_challenge_fields()
        context['form'] = ChallengeForm(
            fields=fields,
            initial={'signature':
                ChallengeDisplayView.signer.sign(
                    ChallengeDisplayView.SIGNATURE_MESSAGE % (
                        timezone.now().isoformat(),
                        seed
                    )
                )
            }
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
        solver_module = importlib.import_module(self.object.solver_script_path, package='home')
        timestamp, seed = verify_signature(data.get('signature', ''))
        if timestamp:
            duration = timezone.now() - datetime.fromisoformat(timestamp)
        else:
            return
        logger.debug(f"started - {timestamp}, finished - {timezone.now()}")
        logger.debug(f"Solution took {duration}.")
        solver = solver_module.Solver(seed, **data)
        attempt = ChallengeAttempt(
            challenge=self.object,
            attempted_by=username,
            attempted_date_time=timestamp,
            score=solver.get_score(duration),
            duration=duration,
            completed=solver.solve(data['solution']),
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


class ContactView(FormView):
    form_class = ContactForm

    def form_valid(self, form):
        print(form)
        return super().form_valid(form)

    def get_success_url(self):
        return HttpResponse(200)

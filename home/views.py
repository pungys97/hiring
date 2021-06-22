import importlib
from collections import defaultdict
from datetime import datetime, timedelta
from django.core.cache import cache
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.core.signing import Signer
from django.db.models import Max, Min, F
from django.http import JsonResponse, HttpResponseBadRequest
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.views import View
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.generic import TemplateView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView
from random_username.generate import generate_username

from hiring.settings import LEAD_RECIPIENTS, GCP
from .forms import ChallengeForm, ContactForm
from .models import Challenge, ChallengeAttempt
from .utils import get_logger, verify_signature

logger = get_logger(__name__)

CACHE_SCORES_KEY = 'scores_cache'
CACHE_SCORES_KEY_VALID_FOR = 10 * 60  # cache for 10 mins


def get_username(request):
    username = request.COOKIES.get('username', generate_username()[0])
    return username.lower()


def published_challenges():
    """
    Returns all published challenges sorted from most recently created to least. Number of published challenges should
    never be too high (more than 5/6) due to layout constraints.
    :return: Queryset of challenges
    """
    return Challenge.objects.filter(is_published=True).order_by('-created_date_time')


def compute_scores():
    published_challenges_ids, published_challenges_score_fields = map(tuple, zip(*published_challenges().values_list('id', 'scoreboard_field')))
    published_challenges_attempts = ChallengeAttempt.objects.filter(challenge__is_published=True)
    max_scores = get_max_scores_for_each_challenge(published_challenges_attempts)
    if GCP:  # works on Postgres only
        scores_by_user = published_challenges_attempts.values('attempted_by', 'challenge').order_by('-score').distinct('attempted_by', 'challenge')
    else:
        scores_by_user = published_challenges_attempts.values('attempted_by', 'challenge').annotate(
            score=Max('score'), duration=Min('duration')
        ).order_by('attempted_by')
    data = defaultdict(lambda: [None for _ in range(len(published_challenges_ids))])  # create initial list of length no.
    # of published challenges == column count, so that the table row has always correct number of columns
    for score in scores_by_user:
        column_idx = published_challenges_ids.index(score['challenge'])  # used to assign proper column in scoreboard table
        show_norm_score = published_challenges_score_fields[column_idx] == 's'  # see details in models.py
        score['score_norm'] = score['score'] / max_scores[score['challenge']]
        score['score_detail_to_show'] = score['score_norm'] if show_norm_score else score['duration']
        user = score.pop('attempted_by')
        data[user][column_idx] = score
    sorted_scores = sorted(
        data.items(),
        key=lambda x: sum(y['score_norm'] if y else 0 for y in x[1]),
        reverse=True
    )
    return sorted_scores


def get_max_scores_for_each_challenge(published_challenges_attempts):
    max_scores = published_challenges_attempts.values('challenge').annotate(max_score=Max('score'))
    max_scores = {challenge['challenge']: challenge['max_score'] for challenge in max_scores}
    return max_scores


class HomeView(TemplateView):
    template_name = 'home.html'

    @cached_property
    def username(self):
        return get_username(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scores = cache.get(CACHE_SCORES_KEY)
        if not scores:
            logger.debug("Top 5 not cached.")
            scores = compute_scores()
            cache.set(CACHE_SCORES_KEY, scores)
        context['top_5'] = scores[:5]
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
        scores = compute_scores()
        paginator = Paginator(scores, 20)
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
        generator_module = importlib.import_module(self.object.generator_script_import_statement, package='home')
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
        solver_module = importlib.import_module(self.object.solver_script_import_statement, package='home')
        timestamp, seed = verify_signature(data.get('signature', ''))
        if timestamp:
            duration = timezone.now() - datetime.fromisoformat(timestamp)
        else:
            return
        logger.debug(f"started - {timestamp}, finished - {timezone.now()}")
        logger.debug(f"Solution took {duration}.")
        solver = solver_module.Solver(seed, **data)
        completed = solver.check_solution(**data)
        if duration > timedelta(minutes=self.object.time_limit_in_minutes):
            return False  # not completed
        attempt = ChallengeAttempt(
            challenge=self.object,
            attempted_by=username,
            attempted_date_time=timestamp,
            score=solver.get_score(duration, ),
            duration=duration,
            completed=completed,
        )
        if completed:
            attempt.save()
        return completed

    def form_valid(self, form):
        completed = self.save_solution_attempt(form.data)
        if not completed:
            return HttpResponseBadRequest()
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
    template_name = 'home.html'  # not used
    form_class = ContactForm

    def form_valid(self, form):
        send_mail(
            'New lead from Automation Challenge',
            '\n'.join([f'{key}: {value}' for key, value in form.cleaned_data.items()]),
            from_email=None,   # defined in settings.py DEFAULT_FROM_EMAIL
            recipient_list=LEAD_RECIPIENTS,
            fail_silently=False,
        )
        return JsonResponse({}, status=200)

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)

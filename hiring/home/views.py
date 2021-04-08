from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView

from .forms import ChallengeForm
from .models import Challenge


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['challenges'] = Challenge.objects.filter(is_published=True).order_by('created_date_time')[:6]
        return context


class ChallengeDisplayView(DetailView):
    template_name = 'solutions/solution_template.html'
    model = Challenge

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ChallengeForm(inputs={"test": "value", "test2": "value"})
        return context


class ChallengeAnswerView(SingleObjectMixin, FormView):
    template_name = 'solutions/solution_template.html'
    form_class = ChallengeForm
    model = Challenge

    # def post(self, request, *args, **kwargs):
    #     # if not request.user.is_authenticated:
    #     #     return HttpResponseForbidden()
    #     self.object = self.get_object()
    #     self.form = self.get_form()
    #     print(self.form)
    #     return super().post(request, *args, **kwargs)
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        print(form.cleaned_data.get('solution', None))
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

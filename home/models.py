import os

from django.conf import settings
from django.db import models
from django.urls import reverse

from hiring.settings import BASE_DIR
from home.utils import create_if_file_not_exists


class Challenge(models.Model):
    SCOREBOARD_RESULTS_CHOICES = (
        ('t', 'Duration'),
        ('s', 'Score')
    )

    name = models.CharField(max_length=50, blank=False)
    description = models.TextField(blank=True)
    solver_script_import_statement = models.CharField(max_length=255, default="", blank=True)
    generator_script_import_statement = models.CharField(max_length=255, default="", blank=True)
    assignment_modal_template_path = models.CharField(max_length=255, default="", blank=True)
    image_src_path = models.CharField(max_length=255, default="", blank=True)
    created_date_time = models.DateTimeField(auto_now_add=True, auto_created=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    is_published = models.BooleanField(default=False)
    is_timed = models.BooleanField(default=True)
    max_score = models.FloatField()
    number_of_attempts = models.IntegerField(default=-1)
    time_limit_in_minutes = models.IntegerField(default=10)
    slug = models.SlugField(blank=True)
    scoreboard_field = models.CharField(max_length=1, default='s', choices=SCOREBOARD_RESULTS_CHOICES)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('challenge_detail', kwargs={'slug': self.slug})  # new

    def save(self, *args, **kwargs):
        self.slug = '_'.join(str(self.name).lower().split(' '))
        self.solver_script_import_statement = self.solver_script_import_statement if self.solver_script_import_statement != '' else f'.solvers.{self.slug}_solver'
        self.generator_script_import_statement = self.generator_script_import_statement if self.generator_script_import_statement != '' else f'.generators.{self.slug}_generator'
        self.assignment_modal_template_path = self.assignment_modal_template_path if self.assignment_modal_template_path != '' else f'assignments/{self.slug}_modal.html'
        self.image_src_path = self.image_src_path if self.image_src_path != '' else f'/assets/img/portfolio/{self.slug}.png'
        if not self.pk:  # This code only happens if the objects is not in the database yet.
            for file in [
                f'home/solvers/{self.slug}_solver.py',
                f'home/generators/{self.slug}_generator.py',
                f'home/templates/assignments/{self.slug}_modal.html'
            ]:
                create_if_file_not_exists(os.path.join(BASE_DIR, file))
        super().save(*args, **kwargs)


class ChallengeAttempt(models.Model):
    challenge = models.ForeignKey(Challenge, related_name='attempts', on_delete=models.CASCADE)
    attempted_by = models.CharField(max_length=32)
    attempted_date_time = models.DateTimeField(editable=False)
    score = models.FloatField()
    duration = models.DurationField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.challenge.name} by {self.attempted_by} on {self.attempted_date_time}"

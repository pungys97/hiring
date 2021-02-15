from datetime import timedelta

from django.conf import settings
from django.db import models


class Challenge(models.Model):
    name = models.CharField(max_length=50, blank=False)
    description = models.TextField()
    path_to_solver_script = models.URLField(verbose_name='solver')
    template_url = models.CharField(verbose_name='template', max_length=255)
    created_date_time = models.DateTimeField(auto_created=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    is_published = models.BooleanField(default=False)
    is_timed = models.BooleanField(default=True)
    max_score = models.FloatField()
    time_out = models.DurationField(default=timedelta(minutes=10))


class ChallengeAttempt(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    attempted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    attempted_date_time = models.DateTimeField(auto_created=True, editable=False)
    score = models.FloatField()
    duration = models.DurationField(blank=True, null=True)
    completed = models.BooleanField(default=False)

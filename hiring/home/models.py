from datetime import timedelta

from django.conf import settings
from django.db import models


class Challenge(models.Model):
    name = models.CharField(max_length=50, blank=False)
    description = models.TextField(blank=True)
    solver_script_path = models.CharField(verbose_name='solver', max_length=255, default="")
    modal_template_path = models.CharField(verbose_name='modal', max_length=255, default="")
    image_src_path = models.CharField(verbose_name='image', max_length=255, default="")
    created_date_time = models.DateTimeField(auto_now_add=True, auto_created=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    is_published = models.BooleanField(default=False)
    is_timed = models.BooleanField(default=True)
    max_score = models.FloatField()
    number_of_attempts = models.IntegerField(default=-1)
    time_out = models.DurationField(default=timedelta(minutes=10))
    challenge_api_url = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.name


class ChallengeAttempt(models.Model):
    challenge = models.ForeignKey(Challenge, related_name='attempts', on_delete=models.CASCADE)
    attempted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    attempted_date_time = models.DateTimeField(auto_created=True, editable=False)
    score = models.FloatField()
    duration = models.DurationField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.challenge.name} by {self.attempted_by.name} on {self.attempted_date_time}"

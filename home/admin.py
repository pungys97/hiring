from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html

from .models import ChallengeAttempt, Challenge


class ChallengeAttemptInline(admin.TabularInline):
    model = ChallengeAttempt


class ChallengeAdmin(admin.ModelAdmin):
    inlines = [
        ChallengeAttemptInline,
    ]

    list_display = ('name', 'participants', 'total_attempts', 'is_published',)
    list_editable = ('is_published', )

    def participants(self, obj):
        return format_html(
            '<span>{}</span>',
            ChallengeAttempt.objects.filter(id=obj.id).aggregate(Count('attempted_by', distinct=True))['attempted_by__count'],
        )

    def total_attempts(self, obj):
        return format_html(
            '<span>{}</span>',
            obj.attempts.distinct().count(),
        )


admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(ChallengeAttempt)

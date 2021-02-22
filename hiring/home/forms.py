from django import forms


class ChallengeForm(forms.Form):
    solution = forms.CharField(
        widget=forms.Textarea,
        required=True
    )


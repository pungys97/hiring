from django import forms


class LogCabinForm(forms.Form):
    solution = forms.CharField(
        widget=forms.Textarea,
        required=True
    )


from django import forms


class ChallengeForm(forms.Form):
    solution = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'ascii-art',  # same size chars
            }
        ),
        required=True
    )

    def __init__(self, *args, **kwargs):
        inputs = kwargs.pop('inputs', {})
        super().__init__(*args, **kwargs)
        for input_name, input_value in inputs.items():
            self.fields[input_name] = forms.CharField(required=True, initial=input_value)
            self.fields[input_name].disabled = True

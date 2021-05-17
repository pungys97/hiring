from django import forms


class ChallengeForm(forms.Form):
    timestamp = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        """
        :param kwargs:
            fields
                - iterable of Fields that should be shown (ordered)
                - should contain Field objects
            solution_formfield
                - form.Field that should be used as default solution widget
                - default solution = forms.CharField(
                    widget=forms.Textarea(
                        attrs={
                            'class': 'form-control ascii-art',  # same size chars
                        }
                    ),
                    required=True
                )
        """
        fields = kwargs.pop('fields', ())
        super().__init__(*args, **kwargs)
        for field in fields:
            self.fields[field.name] = field.widget
import phonenumbers
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from home.utils import get_logger

logger = get_logger(__name__)


def validate_phone(value):
    error = ValidationError(
            _('%(value)s is not a valid phone number'),
            params={'value': value},
        )
    logger.debug(f'{value} - phone number to be validated')
    try:
        number = phonenumbers.parse(value, None)
    except:
        raise error
    if not number:
        raise error


class ChallengeForm(forms.Form):
    signature = forms.CharField(widget=forms.HiddenInput(), label="")

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


class ContactForm(forms.Form):
    name = forms.CharField(max_length=128)
    email = forms.EmailField()
    phone = forms.CharField(max_length=13, validators=[validate_phone])
    message = forms.CharField(widget=forms.Textarea)

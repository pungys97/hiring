from django import forms


class Field:
    INPUT = 'input'
    SOLUTION = 'solution'

    def __init__(self, name: str, field_type: str, value: str = None):
        self.name = name
        assert field_type in (self.INPUT, self.SOLUTION), "Field type must be either input or solution."
        self.field_type = field_type
        assert field_type == self.INPUT and value or field_type == self.SOLUTION, f"Inputs cannot have empty value."
        self.value = value

    @property
    def is_input(self):
        return self.field_type == self.INPUT

    @property
    def widget(self):
        if self.is_input:
            field = forms.CharField(
                required=True,
                initial=self.value,
                disabled=True
            )
            field.widget.attrs.update({'class': 'form-control'})
        else:
            field = forms.CharField(
                widget=forms.Textarea(
                    attrs={
                        'class': 'form-control ascii-art',  # same size chars
                    }
                ),
                required=True
            )
        return field

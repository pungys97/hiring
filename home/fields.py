from django import forms


class Field:
    INPUT = 'input'
    SOLUTION = 'solution'

    def __init__(self, name: str, field_type: str, value: str = None, single_line: bool = None):
        self.name = name
        assert field_type in (self.INPUT, self.SOLUTION), "Field type must be either input or solution."
        self.field_type = field_type
        assert field_type != self.INPUT or value, f"Inputs cannot have empty value."
        self.value = value
        self.single_line = single_line

    @property
    def is_input(self):
        return self.field_type == self.INPUT

    @property
    def is_multi_line(self):
        if self.single_line is None: # if not defined
            if self.is_input:    # input single line by default
                return False
            return True
        return not self.single_line

    @property
    def widget(self):
        field = forms.CharField(
            required=True,
            initial=self.value if self.is_input else None,
        )
        field.widget.attrs.update({'class': 'form-control'})
        if self.is_multi_line:
            print("tu som")
            field.widget = forms.Textarea(
                attrs={
                    'class': 'form-control ascii-art',  # same size chars
                }
            )
        if self.is_input:
            field.widget.attrs.update({'class': 'form-control', 'readonly': True})
        return field

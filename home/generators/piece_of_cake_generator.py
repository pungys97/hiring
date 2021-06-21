from .base_generator import BaseGenerator
from ..fields import Field


class Generator(BaseGenerator):
    def __init__(self, *args, seed=None, **kwargs):
        super().__init__(*args, seed=seed, **kwargs)
        self.text = "ljlfjlekjdjaksdjakjdakjdlksjdlakjdsladjlkasdasjdlkasjdksadlksajdklsadkjasdjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj"
        self.word = self.rng.randrange(5, 51)
        self.brackets = '{}'

    def generate_challenge_fields(self):
        return (
                   Field(name='text', value=self.text, field_type=Field.INPUT, single_line=False),
                   Field(name='word', value=self.word, field_type=Field.INPUT),
                   Field(name='brackets', value=self.brackets, field_type=Field.INPUT),
                   Field(name='count', field_type=Field.SOLUTION, single_line=True),
                   Field(name='first occurrence', field_type=Field.SOLUTION, single_line=True),
                   Field(name='count enclosed', field_type=Field.SOLUTION, single_line=True),
               ), self.seed

    def get_fields(self) -> dict:
        return {
            'width': self.width,
            'height': self.height
        }
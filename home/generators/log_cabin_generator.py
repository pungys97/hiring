from .base_generator import BaseGenerator
from ..fields import Field


class Generator(BaseGenerator):
    def __init__(self, *args, seed=None, **kwargs):
        super().__init__(*args, seed=seed, **kwargs)
        self.width = self.rng.randrange(5, 50, 2)
        self.height = self.rng.randrange(5, 51)

    def generate_challenge_fields(self):
        return (
                   Field(name='width', value=self.width, field_type=Field.INPUT),
                   Field(name='height', value=self.height, field_type=Field.INPUT),
                   Field(name='solution', field_type=Field.SOLUTION),
               ), self.seed
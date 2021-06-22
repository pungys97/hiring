import re
from datetime import timedelta

from .base_solver import BaseSolver
from ..generators.piece_of_cake_generator import Generator


class Solver(BaseSolver):
    required_params = ('text', 'word', 'brackets', )

    def get_score(self, duration, **kwargs):
        benchmark_duration = timedelta(minutes=1)
        return benchmark_duration/duration * 100

    def check_solution(self, **kwargs):
        return self._check_count(int(kwargs.get('count')[0])) \
               and self._check_first_occurrence(int(kwargs.get('first occurrence')[0]))\
               and self._check_count_within_brackets(int(kwargs.get('count enclosed')[0]))

    def __init__(self, seed, **kwargs):
        super().__init__()
        assert all([required_param in kwargs.keys() for required_param in Solver.required_params]), "Not all required arguments were filled."
        generator = Generator(seed=int(seed))
        self.text = kwargs.get("text")[0]
        assert self.text == generator.text, f"Text - {self.text} from the form does not correspond to generated one - {generator.text}."
        self.word = kwargs.get("word")[0]
        assert self.word == generator.word, f"Word - {self.word} from the form does not correspond to generated one - {generator.word}."
        self.brackets = kwargs.get("brackets")[0]
        assert self.brackets == generator.brackets, f"Brackets - {self.brackets} from the form does not correspond to generated one - {generator.brackets}."

    def _check_count(self, count):
        return self.text.count(self.word) == count

    def _check_first_occurrence(self, appearance):
        return self.text.index(self.word) == appearance

    def _check_count_within_brackets(self, count):
        left, right = self.brackets
        return self.text.count(f"{left}{self.word}{right}") == count

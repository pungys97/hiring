from typing import Tuple, Union

from .base_generator import BaseGenerator
from ..fields import Field


class Generator(BaseGenerator):
    BRACKETS = ['{}', '[]', '()']
    WORDS = ('foo', 'bar', 'moo', 'app', 'apple', 'banana', 'orange', 'spinach', 'hello', 'mellow',
                 'yellow', 'black', 'cat', 'hat', 'sad', 'mad', 'low', 'dump', 'jump', 'lamp')

    def __init__(self, *args, seed=None, **kwargs):
        super().__init__(*args, seed=seed, **kwargs)
        self.text, self.word, self.brackets = self._generate_challenge()

    def generate_challenge_fields(self):
        return (
                   Field(name='text', value=self.text, field_type=Field.INPUT, single_line=False),
                   Field(name='word', value=self.word, field_type=Field.INPUT),
                   Field(name='brackets', value=self.brackets, field_type=Field.INPUT),
                   Field(name='count', field_type=Field.SOLUTION, single_line=True),
                   Field(name='first occurrence', field_type=Field.SOLUTION, single_line=True),
                   Field(name='count enclosed', field_type=Field.SOLUTION, single_line=True),
               ), self.seed

    def _generate_challenge(self, word_count: int = 1000, words: Tuple[str, ...] = WORDS) -> Tuple[str, str, str]:
        text_tmp = self.rng.choices(words, k=word_count)
        idx, text = 0, []
        while idx < word_count - 1:
            left, right = text_tmp[idx], text_tmp[idx+1]
            ret = self._randomly_join(left, right)
            if type(ret) == str:  # joined --> skip 2
                ret = (ret, )
                idx += 1
            text.extend(ret)
            idx += 1
        text = " ".join(map(self._randomly_surround_with_brackets, text))
        word = str(self.rng.choice(words))
        bracket = str(self.rng.choice(self.BRACKETS))

        return text, word, bracket

    def _randomly_surround_with_brackets(self, word: str) -> str:
        brackets_or_none = self.rng.choice([self.rng.choice(self.BRACKETS), None, None])  # 1:2 chance of being enclosed in brackets
        if brackets_or_none is None:
            return word
        return f"{brackets_or_none[0]}{word}{brackets_or_none[1]}"

    def _randomly_join(self, word1: str, word2: str) -> Union[str, Tuple[str, str]]:
        join_character = self.rng.choice(['-', '_', None, None, None, None])
        if join_character is None:
            return word1, word2
        return f"{word1}{join_character}{word2}"

import random
import sys
from abc import ABC, abstractmethod


class BaseGenerator(ABC):
    """
    Boilerplate for challenge generators. All generators need to implement generate.
    """

    @abstractmethod
    def __init__(self, *args, seed=None, **kwargs):
        """
        This class is instantiated with form.data received in POST request from the challenge form. It is important that
        the required arguments are named exactly as the formfields.
        :param kwargs: all data is passed from the form, additional logic to handle required fields should be implemented locally
        """
        super().__init__(*args, **kwargs)
        self.seed = random.randrange(sys.maxsize) if not seed else seed
        print(f"seed base = {self.seed}")
        self.rng = random.Random(self.seed)

    @abstractmethod
    def generate_challenge_fields(self) -> (tuple, int):
        """
        Generate random assignment for given Challenge.
        :return: returns tuple (iterable) of Fields and seed used for initialization.
        """
        pass

    @abstractmethod
    def get_fields(self) -> dict:
        """
        Generate dictionary of fields: value for given seed.
        :return: dict.
        """
        pass
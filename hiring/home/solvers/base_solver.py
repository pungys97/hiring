from abc import ABC, abstractmethod
from datetime import timedelta


class BaseSolver(ABC):
    """
    Boilerplate for challenge solvers. All solvers need to implement solve and get_score.
    """

    @abstractmethod
    def __init__(self):
        """
        This class is instantiated with form.data received in POST request from the challenge form. It is important that
        the required arguments are named exactly as the formfields.
        :param kwargs: all data is passed from the form, additional logic to handle required fields should be implemented locally
        """
        super().__init__()

    @abstractmethod
    def solve(self, solution):
        pass

    @abstractmethod
    def get_score(self, duration: timedelta) -> float:
        pass

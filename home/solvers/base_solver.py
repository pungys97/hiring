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
    def check_solution(self, solution):
        pass

    @abstractmethod
    def get_score(self, **kwargs) -> float:
        """
        Should return a float number representing score in descending fashion. 1st has the highest last the lowest.
        :param kwargs: any value required to determine the score
        :return: score
        """
        pass

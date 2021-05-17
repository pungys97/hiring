from abc import ABC, abstractmethod


class BaseSolver(ABC):
    """
    Boilerplate for challenge solvers. All solvers need to implement solve and get_score.
    """
    @abstractmethod
    def __init__(self, **kwargs):
        """
        This class is instantiated with form.data received in POST request from the challenge form. It is important that
        the required arguments are named exactly as the formfields.
        :param kwargs: all data is passed from the form, additional logic to handle required fields should be implemented locally
        """
        pass

    @abstractmethod
    def solve(self, solution):
        pass

    @abstractmethod
    def get_score(self, *args, **kwargs):
        pass

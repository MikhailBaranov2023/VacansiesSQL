from abc import ABC, abstractmethod


class AbstractAPIEngine(ABC):
    """
    Реализован абстрактрый класс для получения данных через API
    """
    @abstractmethod
    def get_vacancies_data(self):
        pass

    @abstractmethod
    def get_employer_data(self):
        pass

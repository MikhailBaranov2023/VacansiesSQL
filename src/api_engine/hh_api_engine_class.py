import httpx

from src.api_engine.abstract_engine_class import AbstractAPIEngine
from src.config import hh_api_config


class HH_API_Handler(AbstractAPIEngine):
    """
    Класс для получения информации о вакансиях и работодателях. Возвращает список словарей.
    """
    def __init__(self, page: int = 0) -> None:
        self.url = "https://api.hh.ru/vacancies"
        self.params = {
            "page": page,
            "employer_id": hh_api_config.get('employer_ids'),
            "only_with_salary": hh_api_config.get("only_with_salary"),
            "per_page": hh_api_config.get("vacancies_per_page"),
            "area": hh_api_config.get("area")
        }

    def get_vacancies_data(self) -> list[dict]:
        """
        Функция возвращает информацию о вакансиях.
        :return:
        """
        response = httpx.get(self.url, params=self.params)
        return response.json()['items']

    def get_employer_data(self) -> list[dict]:
        """
        Функция возвращает информацию о работодателях.
        :return:
        """
        employers = []
        for uid in self.params.get('employer_id'):
            if uid is not None:
                employers.append({
                    'id': uid,
                    'name': httpx.get(f'https://api.hh.ru/employers/{uid}').json().get('name'),
                    'url': httpx.get(f'https://api.hh.ru/employers/{uid}').json().get('alternate_url')
                })
        return employers

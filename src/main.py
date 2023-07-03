import os
from src.db_manage.db_manager import PostgressDBManager
from src.api_engine.hh_api_engine_class import HH_API_Handler
from src.utils import insert_employer_data_to_db, insert_vacancy_data_to_db

if __name__ == '__main__':
    db = PostgressDBManager(
        dbname='coursework',
        user='postgres',
        password='problema99',
        host="localhost",
        port="5432"
    )
    db.drop_tables()
    db.create_tables()

    api_handler = HH_API_Handler()
    vacancy_list = api_handler.get_vacancies_data()
    employers_list = api_handler.get_employer_data()

    insert_employer_data_to_db(employers_list, db)
    insert_vacancy_data_to_db(vacancy_list, db)

    print(db.get_companies_and_vacancies_count())
    print(db.get_all_vacancies())
    print(db.get_avg_salary())
    print(db.get_vacancies_with_higher_salary())
    print(db.get_vacancies_with_keyword("Фасовщик"))

    if not db.conn.closed:
        db.conn.close()

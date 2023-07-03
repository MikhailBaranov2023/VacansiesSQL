import os
from src.db_manage.db_manager import PostgresDBManager
from src.api_engine.hh_api_engine_class import HH_API_Handler
from src.utils import insert_employer_data_to_db, insert_vacancy_data_to_db
from dotenv import load_dotenv

if __name__ == '__main__':

    load_dotenv()

    db = PostgresDBManager(
        dbname='coursework',
        user='postgres',
        password=os.environ.get('DB_PASSWORD'),
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

    user_input = int(input("""
        Доступны следующие функции:
        1 - получаете список всех компаний и количество вакансий у каждой компании.
        2 - получаете список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        3 - получаете среднюю зарплату по вакансиям.
        4 - получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        5 - получает список всех вакансий, в названии которых содержатся переданное слово.
        0 - Выход.
    """))
    print(user_input)
    while True:
        if user_input == 1:
            print(db.get_companies_and_vacancies_count())
            user_input = int(input())
        elif user_input == 2:
            print(db.get_all_vacancies())
            user_input = int(input())
        elif user_input == 3:
            print(db.get_avg_salary())
            user_input = int(input())
        elif user_input == 4:
            print(db.get_vacancies_with_higher_salary())
            user_input = int(input())
        elif user_input == 5:
            input_word = str(input("Введите слово для поиска").upper())
            print(db.get_vacancies_with_keyword(input_word))
            user_input = int(input(""))
        elif user_input == 0:
            break

    if not db.conn.closed:
        db.conn.close()

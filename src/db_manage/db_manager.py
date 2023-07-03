import psycopg2
from src.db_manage.abstarc_db_manager import AbstractDBManager


class PostgressDBManager(AbstractDBManager):
    def __init__(self, dbname, user, password, host, port):
        self.conn = psycopg2.connect(database=dbname,
                                     user=user,
                                     password=password,
                                     host=host,
                                     port=port)

    def create_tables(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS companies (
                id INT PRIMARY KEY,
                NAME TEXT NOT NULL,
                url VARCHAR(100)
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                id INT PRIMARY KEY,
                name TEXT NOT NULL,
                company_id INT REFERENCES companies(id) ON DELETE CASCADE,
                salary_min INT,
                salary_max INT,
                url VARCHAR(100)
                );
            """)
            self.conn.commit()

    def drop_tables(self):
        with self.conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS vacancies;")
            cur.execute("DROP TABLE IF EXISTS companies;")
            self.conn.commit()

    def get_companies_and_vacancies_count(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT companies.name, COUNT(vacancies.id)
                FROM companies
                JOIN vacancies ON companies.id = vacancies.company_id
                GROUP BY companies.name;
            """)
            return cur.fetchall()

    def get_all_vacancies(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT companies.name, vacancies.name, vacancies.salary_min, vacancies.salary_max, vacancies.url
                FROM vacancies
                JOIN companies ON vacancies.company_id = companies.id;
            """)
            return cur.fetchall()

    def get_avg_salary(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT AVG(salary_min + salary_max) / 2
                FROM vacancies;
            """)
            return cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        with self.conn.cursor() as cur:
            cur.execute(f"""
                SELECT companies.name, vacancies.name, vacancies.salary_min, vacancies.salary_max, vacancies.url
                FROM vacancies
                JOIN companies ON vacancies.company_id = companies.id
                WHERE ((vacancies.salary_min + vacancies.salary_max) / 2) > {self.get_avg_salary()};
            """)
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        with self.conn.cursor() as cur:
            cur.execute(f"""
                SELECT companies.name, vacancies.name, vacancies.salary_min, vacancies.salary_max, vacancies.url
                FROM vacancies
                JOIN companies ON vacancies.company_id = companies.id
                WHERE vacancies.name ILIKE '%{keyword}%' OR companies.name ILIKE '%{keyword}%';
            """)
            return cur.fetchall()

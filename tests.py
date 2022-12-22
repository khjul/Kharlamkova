from unittest import TestCase, main
from main import DataSet, Vacancy, InputConnect

class DataSetTest(TestCase):
    def test_input(self):
        self.assertEqual(DataSet('vacancies_by_year.csv').file_name, "vacancies_by_year.csv")
        self.assertEqual(len(DataSet("vacancies_by_year.csv").vacancies_objects), 0)

class VacancyTests(TestCase):
    def test_vacancy_type(self):
        self.assertEqual(type(Vacancy(args=['Программист баз данных', '36000', '50000', 'RUR', 'Москва', '2007'])).__name__, "Vacancy")

    def test_vacancy_name(self):
        self.assertEqual(Vacancy(args=['Программист баз данных', '36000', '50000', 'RUR', 'Москва', '2007']).name, "Программист баз данных")

    def test_vacancy_salary_from(self):
        self.assertEqual(Vacancy(args=['Программист баз данных', '36000', '50000', 'RUR', 'Москва', '2007']).salary_from, 36000)

    def test_vacancy_salary_to(self):
        self.assertEqual(Vacancy(args=['Программист баз данных', '36000', '50000', 'RUR', 'Москва', '2007']).salary_to, 50000)

    def test_vacancy_salary_currency(self):
        self.assertEqual(Vacancy(args=['Программист баз данных', '36000', '50000', 'RUR', 'Москва', '2007']).salary_currency, "RUR")

    def test_vacancy_area_name(self):
        self.assertEqual(Vacancy(args=['Программист баз данных', '36000', '50000', 'RUR', 'Москва', '2007']).area_name, "Москва")

    def test_vacancy_published_at(self):
            self.assertEqual(Vacancy(args=['Программист баз данных', '36000', '50000', 'RUR', 'Москва', '2007']).published_at, "2007")

class InputConnectTests(TestCase):
    def test_get_count_vacancies(self):
        dataset = DataSet.get_dataset("vacancies_by_year.csv")
        vacancies_count = InputConnect.get_count_vacancies(dataset, "all")
        self.assertEqual(vacancies_count[2007], 2196)

    def test_get_count_vacancies_by_profession(self):
        dataset = DataSet.get_dataset("vacancies_by_year.csv")
        vacancies_count_prof = InputConnect.get_count_vacancies_by_profession(dataset, "Аналитик")
        self.assertEqual(vacancies_count_prof[2007], 34)

    def test_get_proportion_vacancy_by_cities(self):
        dataset = DataSet.get_dataset("vacancies_by_year.csv")
        vacancy_proportion = InputConnect.get_proportion_vacancy_by_cities(dataset)
        self.assertEqual(vacancy_proportion["Москва"], 300945)
        self.assertEqual(vacancy_proportion["Екатеринбург"], 19199)
        self.assertEqual(vacancy_proportion["Псков"], 1367)
        self.assertEqual(vacancy_proportion["Саратов"], 7528)


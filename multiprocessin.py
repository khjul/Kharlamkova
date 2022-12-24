from _datetime import datetime
import multiprocessing
import pandas as pd
import os

class DataSet:
    """Класс для получения данных из CSV файла.

    Attriburies:
        file_name (str): название файла
        profession (str): профессия
    """
    def __init__(self):
        self.file_name, self.profession = DataSet.get_params()

    @staticmethod
    def get_params():
        """Метод для ввода данных.

        :return: Кортеж с названием файла и профессии
        """
        # file_name = input("Введите название папки с файлами: ")
        # profession = input("Введите название профессии: ")
        file_name = 'csv_split_files'
        profession = "Программист"
        return file_name, profession

    def get_not_multiproc(self):
        """Обрабатывает и данные из файлов и сохраняет без использования многопроцессорности.
        """
        name = os.listdir(self.file_name)
        self.data = map(self.get_data_file, name)

    def get_multiproc(self):
        """Обрабатывает и данные из файлов и сохраняет, используя многопроцессорность.
        """
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as p:
            name = os.listdir(self.file_name)
            self.data = p.map(self.get_data_file, name)

    def get_data_file(self, file_name):
        """Возвращает данные файла
		Attributes:
			file_name (str): Название файла

        :param file_name:
        :return: year (int): год публикации
			    mid_salary (int): средня зп
			    count_vacanies (int): количество вакансий
		        mid_prof_salary (int): средняя зп выбранной профессии
			    count_vacanies_by_prof (int): количество вакансий выбранной профессии
        """
        file = pd.read_csv(f'{self.file_name}/{file_name}')
        data = file[file['name'].str.contains(self.profession)]
        years = file['published_at'].apply(lambda x: x[:4]).unique()
        year = years[0]
        mid_salary = round(file.apply(lambda x: (x['salary_from'] + x['salary_to']) * 0.5, axis=1).mean())
        count_vacanies = file.shape[0]
        mid_prof_salary = round(data.apply(lambda x: (x['salary_from'] + x['salary_to']) * 0.5, axis=1).mean())
        count_vacanies_by_prof = data.shape[0]
        return year, mid_salary, count_vacanies, mid_prof_salary, count_vacanies_by_prof

    def get_data_dict(self):
        """Разбивает данные на словари, где
                                            ключ: год
                                            значение: средняя зп / количество вакансий / средняя зп выбранной профессии / кол-во вакансий выбранной профессии
		"""
        mid_salary_by_year_d = dict()
        count_vacancies_by_year_d = dict()
        mid_prof_salary_by_year_d = dict()
        count_vacanies_by_prof_d = dict()
        for year, mid_salary, count_vacanies, mid_prof_salary, count_vacanies_by_prof in self.data:
            mid_salary_by_year_d[year] = mid_salary
            count_vacancies_by_year_d[year] = count_vacanies
            mid_prof_salary_by_year_d[year] = mid_prof_salary
            count_vacanies_by_prof_d[year] = count_vacanies_by_prof
        return mid_salary_by_year_d, count_vacancies_by_year_d,mid_prof_salary_by_year_d,count_vacanies_by_prof_d

    def print(self):
        """Печатает словари.
        """
        dict1, dict2, dict3, dict4 = self.get_data_dict()
        print("Динамика уровня зарплат по годам:", dict1)
        print("Динамика количества вакансий по годам:", dict2)
        print("Динамика уровня зарплат по годам для выбранной профессии:", dict3)
        print("Динамика количества вакансий по годам для выбранной профессии:", dict4)

if __name__ == '__main__':
    start_time = datetime.now()
    data_analitics = DataSet()
    data_analitics.get_not_multiproc()
    data_analitics.print()
    print(f"Time: {datetime.now() - start_time}")

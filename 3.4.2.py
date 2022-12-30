import pandas as pd
from jinja2 import Environment, FileSystemLoader
import pdfkit

class Report:
    ''' Создает отчет в виде pdf-файла.

    Attributes:
        file_name (DataFrame) : файл с данными о вакансиях
        profession (str) : название профессии
    '''
    def __init__(self, file_name, profession):
        '''Инициализирует класс Report

        :param file_name(DataFrame) : файл с данными о вакансиях
        profession (str) : название профессии
        '''
        self.file_name = pd.read_csv(file_name)
        self.profession = profession

    def get_data(self):
        '''Создает словари с информацией по годам.
        :return: salary_vacansies: словарь с зарплатой всех вакансий по годам
        :return: count_vacansies: словарь с количеством всех вакансий по годам
        :return: salary_profession: словарь с зарплатой выбранной профессии по годам
        :return: count_profession: словарь с количеством выбранной профессии по годам
        '''
        self.file_name['year'] = self.file_name['published_at'].apply(lambda x: x[:4])
        years = self.file_name.groupby(['year'])
        salary_vacansies = {}
        count_vacansies = {}
        salary_profession = {}
        count_profession = {}
        for year, data in years:
            salary_vacansies[year] = round(data.apply(lambda x: x['salary'], axis=1).mean())
            count_vacansies[year] = data.shape[0]
            salary_profession[year] = round(data[data['name'].str.contains(self.profession, case=False)].apply(lambda x: x['salary'], axis=1).mean())
            count_profession[year] = data[data['name'].str.contains(self.profession, case=False)].shape[0]
        return salary_vacansies, count_vacansies, salary_profession, count_profession

    def make_pdf(self):
        '''Создает отчет в виде pdf-файла
        :return: отчет в виде pdf-файла с аналитикой с 2003г по 2022г.
        '''
        salary_vacansies, count_vacansies, salary_profession, count_profession = self.get_data()
        template = Environment(loader=FileSystemLoader('.')).get_template('pdf_template(3.4.2).html')
        data = [[year, salary_vacansies[year], salary_profession[year], count_vacansies[year], count_profession[year]] for year in salary_vacansies]
        pdf_template = template.render({'profession': self.profession, 'data': data})
        config = pdfkit.configuration(wkhtmltopdf=r'C:\Users\kh_ju\homework python\wkhtmltopdf\bin\wkhtmltopdf.exe')
        pdfkit.from_string(pdf_template, 'report(3.4.2).pdf', configuration=config, options={"enable-local-file-access": ""})

# file_name = 'full_converted_vacancies_dif_currencies(3.4.1).csv'
# profession = "Аналитик"
file_name = input('Введите название файла: ')
profession = input('Введите название профессии: ').lower()
report = Report(file_name, profession)
report.make_pdf()

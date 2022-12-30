import pandas as pd
from jinja2 import Environment, FileSystemLoader
import pdfkit


class Report:
    '''Создает отчет в виде pdf-файла.

    Attributes:
        file_name (DataFrame) : файл с данными о вакансиях
        profession (str) : название профессии
        area_name(str): название города
    '''

    def __init__(self, file_name, profession, area_name):
        '''
        Инициализирует класс Report

        :param file_name(DataFrame) : файл с данными о вакансиях
        :param: profession (str) : название профессии
        :param area_name (str): название города
        '''
        self.file_name = pd.read_csv(file_name)
        self.profession = profession
        self.area_name = area_name

    def get_data_area(self):
        '''Создает словари с информацией по всем городам.
        :return salary_profession: словарь с аналитикой по зарплате выбранной профессии
        :return count_profession: словарь с аналитикой по количеству вакансий выбранной профессии
        '''
        data = self.file_name[
            (self.file_name['name'].str.contains(self.profession, case=False)) & (self.file_name['area_name'] == self.area_name)]
        data['year'] = data['published_at'].apply(lambda x: x[:4])
        salary_profession = {}
        count_profession = {}
        for year, data in data.groupby(['year']):
            salary_profession[year] = round(data['salary'].mean())
            count_profession[year] = data.shape[0]
        return salary_profession, count_profession

    def get_data_areas(self):
        '''Создает словари с информацией по всем городам.
        :return salary_area_dict: словарь с аналитикой по зарплатам по топ 10 городам
        :return top_area_proportion: словарь с аналитикой по количествам вакансий по топ 10 городам
        '''
        area_proportion = dict(filter(lambda x: x[-1] > 0.01, [(k, round(v / self.file_name.shape[0], 4))
                                                               for k, v in self.file_name['area_name'].value_counts().to_dict().items()]))
        top_area_proportion = dict(list(area_proportion.items())[:10])
        vacancies_area = self.file_name.groupby(['area_name'])
        salary_by_area = {area: round(data['salary'].mean()) for area, data in vacancies_area if area in area_proportion}
        salary_area_dict = dict(sorted(salary_by_area.items(), key=lambda x: x[-1], reverse=True)[:10])
        return salary_area_dict, top_area_proportion


    def make_pdf(self):
        '''Создает отчет в виде pdf-файла
        :return: отчет в виде pdf-файла с аналитикой с 2003г по 2022г.
        '''
        salary_profession, count_profession = self.get_data_area()
        salary_area_dict, top_area_proportion = self.get_data_areas()
        template = Environment(loader=FileSystemLoader('.')).get_template('pdf_template(3.4.3).html')
        table1 = [[year, salary_profession[year], count_profession[year]] for year in count_profession]
        pdf_template = template.render({'profession': self.profession, 'area': self.area_name, 'table1': table1,
                                        'salary_area': salary_area_dict.items(),
                                        'top_area_proportion': top_area_proportion.items()})
        config = pdfkit.configuration(wkhtmltopdf=r'C:\Users\kh_ju\homework python\wkhtmltopdf\bin\wkhtmltopdf.exe')
        pdfkit.from_string(pdf_template, 'report(3.4.3).pdf', configuration=config, options={"enable-local-file-access": ""})

file_name = input('Введите название файла: ')
profession = input('Введите название профессии: ').lower()
area_name = input('Введите название региона: ')
report = Report(file_name, profession, area_name)
report.make_pdf()

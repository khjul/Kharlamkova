import pandas as pd
import numpy as np
import grequests
from datetime import datetime
from xml.etree import ElementTree


class Currency:
    """Класс для формирования CSV-файла с курсами валют.

    Attributes:
        file_name (str): Название файла
        data (str): строки csv-файла
    """

    def __init__(self, data):
        """Инициализирует объект Currency.
        """
        self.file_name = "vacancies_dif_currencies.csv"
        self.data = data[pd.notnull(data['salary_currency'])]

    def get_most_common_currency(self):
        """Создает список валют, которые не являются рублями и встречаются в более чем в 5000 вакансий

        :return: list: список названий валют
        """
        most_common_currency = []
        for key, value in self.data['salary_currency'].value_counts().to_dict().items():
            if key != 'RUR' and value > 5000:
                most_common_currency.append(key)
        return most_common_currency

    def print_frequency_currency(self):
        """Печатает частотность валют в файле.
        """
        df = pd.read_csv(self.file_name)
        print(df["salary_currency"].value_counts())

    def get_urls(self, list_dates, dict_for_csv):
        """
        Создает список urls
        :param list_dates: Список с датами
        :param dict_for_csv: Словарь с данными
        :return: list: Список urls
        """
        urls = []
        for date in list_dates:
            d = pd.to_datetime(str(date))
            dict_for_csv["dat"].append(d.strftime('%Y-%m'))
            urls.append(rf"http://www.cbr.ru/scripts/XML_daily.asp?date_req={d.strftime('%d/%m/%Y')}")
        return urls

    def get_data_for_csv(self):
        """Отбирает данные для создания CSV-файла.

        :return: titles: список названий валют,
                dict_for_csv: словарь для сбора данных,
                list_dates: список с датами
        """
        dataFrame = pd.read_csv(self.file_name)
        dataFrame["published_at"] = dataFrame["published_at"].apply(lambda x: datetime(int(x[:4]), int(x[5:7]), 1))
        from_date = dataFrame["published_at"].min()
        to_date = dataFrame["published_at"].max()
        titles = self.get_most_common_currency()
        dict_for_csv = {item: [] for item in np.insert(titles, 0, 'dat')}
        list_dates = pd.date_range(from_date.strftime("%Y-%m"), to_date.strftime("%Y-%m"), freq="MS")
        return titles, dict_for_csv, list_dates

    def make_csv(self):
        """Создает DataFrame с информацией о валютах и сохраняет в CSV-файл.
        """
        titles, dict_for_csv, list_dates = self.get_data_for_csv()
        urls = self.get_urls(list_dates, dict_for_csv)
        for response in grequests.map((grequests.get(url) for url in urls)):
            data = {}
            root = ElementTree.fromstring(response.content)
            for element in root.iter('Valute'):
                data_currency = []
                for child in element:
                    data_currency.append(child.text)
                if data_currency[1] in titles:
                    data[data_currency[1]] = round(float(data_currency[4].replace(',', '.')) / int(data_currency[2]), 6)
            for key in titles:
                if key in data:
                    dict_for_csv[key].append(data[key])
                else:
                    dict_for_csv[key].append(None)

        dataFrame = pd.DataFrame(dict_for_csv)
        dataFrame.to_csv("currency_2003-2022.csv", index=False, encoding='utf-8-sig')
        self.print_frequency_currency()


file_name = 'vacancies_dif_currencies.csv'
if __name__ == '__main__':
    dataframe = Currency(pd.read_csv(file_name))
    dataframe.make_csv()

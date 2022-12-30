import numpy as np
import pandas as pd

class Converter:
    """Конвертирует оклад в рубли.
    Attribures:
            file_name (DataFrame) : исходный файл
            converter_file_name (DataFrame) : файл для преобразования валют
    """
    def __init__(self, file_name, converter_file_name):
        """Инициализирует класс Converter
        """
        self.file_name = pd.read_csv(file_name)
        self.converter_file_name = pd.read_csv(converter_file_name)

    def converter(self, salary, converter_file):
        """Возращает сковертированную зарплату по указанной дате.
        :param salary: зарплата
        :param: converter_file: файл для преобразования валют
        :return: сконвертированная зарплата
        """
        data = salary.split()
        currency = data[1]
        if currency in converter_file.columns:
            date = data[2]
            course = converter_file[converter_file["dat"] == date[:7]][currency].values
            if not np.isnan(course[0]):
                return round(course[0] * float(data[0]))
        return salary
    def get_converted_data(self):
        """Подготавливает данные для CSV-файла.
        """
        self.file_name.insert(1, "salary", None)
        self.file_name["salary"] = self.file_name[["salary_from", "salary_to"]].mean(axis=1)
        self.file_name["salary"] = self.file_name["salary"].astype(str) + " " + + self.file_name["salary_currency"] + " " + self.file_name["published_at"]
        self.file_name["salary"] = self.file_name["salary"].apply(lambda salary: self.converter(salary, self.converter_file_name))

        self.file_name = self.file_name.drop(columns=['salary_from', 'salary_to', 'salary_currency'])

    def make_csv(self):
        """Создает CSV-файл.
        """
        self.get_converted_data()
        converted_currencies = self.file_name.head(4074961)
        converted_currencies.to_csv("full_converted_vacancies_dif_currencies(3.4.1).csv", index=False, encoding='utf-8-sig')

file_name = "vacancies_dif_currencies.csv"
converter_file_name = "currency_2003-2022.csv"
if __name__ == '__main__':
    converter = Converter(file_name=file_name, converter_file_name=converter_file_name)
    converter.make_csv()

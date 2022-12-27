import requests
from pandas import json_normalize

urls = []
urls += [
    f'https://api.hh.ru/vacancies?specialization=1&per_page=100&page={page}&date_from=2022-12-25T00:00:00&date_to=2022-12-25T08:00:00'
    for page in range(20)]
urls += [
    f'https://api.hh.ru/vacancies?specialization=1&per_page=100&page={page}&date_from=2022-12-25T08:00:00&date_to=2022-12-25T16:00:00'
    for page in range(20)]
urls += [
    f'https://api.hh.ru/vacancies?specialization=1&per_page=100&page={page}&date_from=2022-12-25T16:00:00&date_to=2022-12-26T00:00:00'
    for page in range(20)]

vacancies = []
for url in urls:
    vacancy = requests.get(url).json()
    vacancies.extend(vacancy["items"])

dataFrame = json_normalize(vacancies)
vacanciesHH = dataFrame[["name", "salary.from", "salary.to", "salary.currency", "area.name", "published_at"]]
vacanciesHH.to_csv("vacanciesHH_2022-12-25.csv", index=False, encoding='utf-8-sig')
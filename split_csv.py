import pandas as pd
import threading

class Split_CSV:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = pd.read_csv(file_name)

    @staticmethod
    def to_csv(data: pd.DataFrame, file_name):
        data.to_csv(path_or_buf=file_name, index=False, encoding='utf-8-sig')

    def create_chunks(self):
        years = self.data['published_at'].apply(lambda x: x[:4]).unique()
        for year in years:
            right_data = self.data[self.data['published_at'].str.contains(year)]
            t = threading.Thread(target=self.to_csv, args=(right_data, f'csv_split_files/vacancies_by_{year}.csv'))
            t.start()

data = Split_CSV('vacancies_by_year.csv')
data.create_chunks()
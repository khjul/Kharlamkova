import sqlite3
import pandas as pd

con = sqlite3.connect('currency_2003-2022.db')
df = pd.read_csv('currency_2003-2022.csv')
df.to_sql(name='currency_2003-2022', con=sqlite3.connect('currency_2003-2022.db'), index=False)
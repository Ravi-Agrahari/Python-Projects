import pandas as pd 
import csv 
from datetime import datetime 

class CSV:
    CSV_FILE = 'finance_data.csv'
    COLUMNS = ['Date', 'Amount', 'Category', 'Description']

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)


    @classmethod
    def add_data(cls, date , amount, category, description):
        new_entry = {
            'Date': date,
            'Amount': amount,
            'category': category,
            'Description': description
        }
        with open(cls.CSV_FILE, 'a' , newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
            print('Data added successfully')
            



CSV.initialize_csv()

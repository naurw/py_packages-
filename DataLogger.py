import tkinter as tk
from tkinter import messagebox
import os
import pandas as pd
from openpyxl import load_workbook
from time import sleep 


class DataLogger:
    def __init__(self, dataframe, file_name='v3_speed_test_logs.xlsx', directory='v3_logs'):
        self.df = dataframe
        self.current_path = os.getcwd()
        self.file_name = file_name
        self.directory = directory
        self.new_path = ''
        self.gui = tk.Tk() 
        self.gui.withdraw() 

        self.check_directory()
        self.write_to_excel()

    def check_directory(self):
        logs_dir = os.path.join(self.current_path, self.directory)
        if not os.path.exists(logs_dir):
            print(f'File Path: {logs_dir} does not exist... creating directory now')
            message = f'File Path: {logs_dir} does not exist... creating directory now'
            messagebox.showinfo(message=message)
            os.mkdir(logs_dir)
        else:
            print(f'File Path: {logs_dir} exists... changing directory')
            message = f'File Path: {logs_dir} exists... changing directory'
            messagebox.showinfo(message=message)
        os.chdir(logs_dir)
        self.new_path = os.getcwd()
        print(self.new_path)
            
    def write_to_excel(self):
        try:
            file_path = os.path.join(self.new_path, self.file_name)
            if not os.path.exists(file_path):
                message = f'{file_path} does not exist... creating file'
                messagebox.showinfo(title='Warning', message=message)
                self.df.to_excel(self.file_name, index=True)
            else:
                message = f'{file_path} has been found... opening and appending'
                messagebox.showinfo(title='File Found', message=message)

                with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                    self.df.to_excel(writer, sheet_name='Sheet1', index=False)
            os.chdir(os.pardir)
        except Exception as e:
            message = f'Error occurred:\n{e}\n\nRetrying with alternative method'
            messagebox.showinfo(title='Warning', message=message)
            sleep(3)

            with pd.ExcelWriter(self.file_name, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                existing_df = pd.read_excel(self.file_name)
                messagebox.showinfo(title = 'Previous Data', message = f'\n\n{existing_df.tail(5)}')
                book = load_workbook(self.file_name)
                writer.book = book
                writer.sheets = {ws.title: ws for ws in writer.book.worksheets}
                new_df = pd.concat([existing_df, self.df], axis=0, ignore_index=True)
                messagebox.showinfo(title = 'Updated Data', message = f'\n\n{new_df.tail(5)}')
                new_df.to_excel(writer, sheet_name='Sheet1', index=False)
                writer.save()
            os.chdir(os.pardir)


#logger = DataLogger(data, file_name='my_logs.xlsx', directory='my_logs')

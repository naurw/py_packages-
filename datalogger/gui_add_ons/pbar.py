import tkinter as tk 
import os 
import platform 
import subprocess
from time import sleep 
from tkinter import messagebox
from tqdm import tqdm 

class ProgressBar: 
    def __init__(self, file_name='my_logs.xlsx', directory = 'my_logs'): 
        self.gui = tk.Tk()
        self.gui.withdraw() 
        self.file_name = file_name 
        self.new_path = os.getcwd()
        self.directory = directory

        if self.gui.winfo_exists():
            self.gui.event_generate("<<ThemeChanged>>") 

    def find_folder_and_files(self): # recursively iterate over all directories and subdirectories and list the files present 
        file_names = []
        for root, dirs, files in os.walk(self.new_path): 
            if self.directory in dirs: 
                print(f'Directory found: {self.new_path}/{self.directory}')
                self.new_path = os.path.join(root, self.directory)
                for file in os.listdir(self.new_path): 
                    file_names.append(file)
                break
            else: 
                print('Directory not found.')
                return None 
            
        return self.new_path, file_names 

    
    def open_file(self): 
        try: 
            with tqdm(total = 100, desc = 'Opening File', unit = '%', ncols = 70) as pbar: 
                for i in range(100): 
                    pbar.update(1) 
                    sleep(0.03) 
            print(self.new_path)

            answer = messagebox.askyesno(title = 'File Found', message = 'Do you want to open file?')
            if answer: 
                if platform.system() == 'Windows': 
                    os.system(f'start {os.path.join(self.new_path, self.file_name)}')
                elif platform.system() == 'Darwin': 
                    subprocess.run(['open', os.path.join(self.new_path, self.file_name)])
                elif platform.system() == 'Linux': 
                    print('Wow you special')
                    subprocess.run(['xdg-open', os.path.join(self.new_path, self.file_name)]) 

        except FileNotFoundError as e: 
            print(f'Error has occured: {e}') 

        finally: 
            print('Completed')


# pbar = ProgressBar()
# pbar.find_folder()
# pbar.open_file() 

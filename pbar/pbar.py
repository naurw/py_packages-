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
        self.destroyed = False # initialize the flag 
        
        # self.find_folder() 

        if self.gui.winfo_exists():
            self.gui.event_generate("<<ThemeChanged>>") # addresses error when application is closed or destroyed before event being generated is processed. if window has already been destroyed, then event will not be genereated 

    def find_folder(self): # recursively iterate over all directories and subdirectories 
        for root, dirs, files in os.walk(self.new_path): 
            if self.directory in dirs: 
                print(f'Directory found: {self.new_path}/{self.directory}')
                self.new_path = os.path.join(root, self.directory)
                return self.new_path

        return None  
    
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
            if not self.destroyed: # add a flag for handling if .destroyed() 
                self.gui.destroy() 
                self.destroyed = True 
            


        self.gui.mainloop() 


# pbar = ProgressBar()
# pbar.find_folder()
# pbar.open_file() 

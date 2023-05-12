import tkinter as tk 
import os 
import platform 
import subprocess
from time import sleep 
from tkinter import messagebox
from tqdm import tqdm 
from tkinter import ttk

class ProgressBar: 
    def __init__(self, file_name='my_logs.xlsx', directory = 'my_logs'): 
        self.gui = tk.Tk()
        self.gui.geometry('200x200')
        self.gui.withdraw() 
        self.file_name = file_name 
        self.new_path = os.getcwd()
        self.directory = directory
        self.destroyed = False # initialize the flag

        self.progressbar = ttk.Progressbar(self.gui, orient='horizontal', length=200, mode='determinate')
        self.progressbar.pack()

        self.find_folder() 

    def find_folder(self): # recursively iterate over all directories and subdirectories 
        for root, dirs, files in os.walk(self.new_path): 
            if self.directory in dirs: 
                print(f'Directory found: {self.new_path}/{self.directory}')
                self.new_path = os.path.join(root, self.directory)
                return

        return None  

    def open_file(self): 
        try: 
            self.progressbar.start(10) # start the progress bar
            self.progressbar.update() # update the progress bar
            self.progressbar["maximum"] = 100 # set the maximum value for the progress bar
            for i in range(100): 
                self.progressbar["value"] = i+1 # increment the value of the progress bar
                sleep(0.03) 
                self.progressbar.update() # update the progress bar

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
            if not self.destroyed: # check the flag before destroying the GUI
                self.gui.destroy() 
                self.destroyed = True 

    def run(self):
        self.gui.deiconify()
        self.gui.after(0, self.open_file)
        self.gui.mainloop()

pbar = ProgressBar()
pbar.run()

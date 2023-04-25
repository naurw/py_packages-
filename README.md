# py_packages
>Contributor: Will

## 🐍 Contents 🐍 
### `DataLogger.py` ***Current version*** --> v2.3
>DataLogger is a module that enables a simpler way to log data dynamically to an Excel file (with it's own directory based on your current working directory) while optimizing readability for the user.
- Default logging script for `SpeedTest.py` 
  #### What's new?
  - Integrated user inputs with a max threshold to determine columnar sizes 
  - Progress bar with operating system(s) interactions
  - Refined try/except blocks 
  
  #### What's to come?
  - Replacing procedural progress bar with OOP from pbar in v2.3.1
  - Add and create dataframes to an existing Excel file into its own Sheet in v3.1
  - Multi dataframe compiler method with `contextmanager` in the works in v3.1 

### `pbar.py` ***Current version*** --> v1.1 
>ProgressBar is a module that displays a progress bar in the console while interacting with user inputs and operating system(s) to open a file into the user's view. It also serves as a directory verifier to see if user inputs are correct. 
- Default progress bar script for `DataLogger.py` 

### `SpeedTest.py` ***Current version*** --> v4.2 
>SpeedTest is a standalone application that runs network speed test(s) with a data logging functionality. It allows for the user to complain about poor network performances via Twitter.  
  #### What's new? 
  - Standalone application in v4.2 
  
  #### What's to come? 
  - Adjustments to CSS selectors for composing and more consistent window handling in v4.3
  - Use configuration `.ini` files with `configparser` to parse, optimizations with context managers in v5.1

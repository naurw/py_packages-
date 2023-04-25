# py_packages
>Contributor: Will

## 🐍 Contents 🐍 
### `DataLogger.py` ***Current version*** --> v2.2 
>DataLogger is a module that enables a simpler way to log data dynamically to an Excel file (with it's own directory based on your current working directory) while optimizing readability for the user.
- Default logging script for `SpeedTest.py` 
  #### What's new?
  - Dynamically adjust Excel file column width in v2.2 
  - Fixed errors that cause .xlsx file to corrupt and other potential errors that may be raised in v2.2
  
  #### What's to come? 
  - Integrate user inputs to determine whether or not adjustments to cells is desired and create a limit in cell size in v2.3
  - Option to open Excel file at the end after creation in v2.3 
  - Refine try-except error handling in v2.3 
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

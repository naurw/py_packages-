# py_packages
>Contributor: Will

## 🐍 Contents 🐍 
### `DataLogger.py` ***Current version*** --> 2.3.1 🚧 🏗️ 🚧  --> v3.1.1
>DataLogger is a universal class object that enables a more convenient way to log data dynamically to an Excel file while optimizing readability and accessibility for the user. 
- Default logging script for `SpeedTest.py` 
  #### What's new?
  - Integrated user inputs with an input validation to compute ideal columnar sizes 
  - Visual cues/aids with operating system(s) interactions
  - Ingest single or multiple dataframes into a new or existing Excel file with its own sheet per dataframe 
  - Added additional flexibility and refined logic for scalability 
  
  #### What's to come?
  - TBD 

### `pbar.py` ***Current version*** --> v1.1.1 
>ProgressBar is a module that displays a progress bar in the console while interacting with user inputs and operating system(s) to open a file into the user's view. It also serves as a directory verifier to see if user inputs are correct. 
- Default progress bar script for `DataLogger.py` 

### `SpeedTest.py` ***Current version*** --> v4.2 🚧 🏗️ 🚧 --> TBD 
>SpeedTest is a standalone application that runs network speed test(s) with a data logging functionality. It allows for the user to complain about poor network performances via Twitter.  
  #### What's new? 
  - Standalone application in v4.2 
  
  #### What's to come? 
  - Adjustments to CSS selectors for composing and more consistent window handling in v4.2.1
  - Use configuration `.ini` files with `configparser` to parse, optimizations with context managers in v5.1

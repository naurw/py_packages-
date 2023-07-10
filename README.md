# py_packages
>Contributor: Will

## 🐍 Contents 🐍 
## **Packages**
### `datalogger` ***Current version*** --> v3.1.2
>datalogger is a universal package that enables a more convenient way to log data dynamically to an Excel file while optimizing readability and accessibility for the user. 
- Default logging script for `SpeedTest.py` 
  #### What's new?
  - Integrated user inputs with an input validation to compute ideal columnar sizes 
  - Visual cues/aids with operating system(s) interactions
  - Ingest single or multiple dataframes into a new or existing Excel file with its own sheet per dataframe 
  - Added additional flexibility by breaking functions into subfunctions and refined logic for scalability 
  - Highlights newly concatenated records with each revision of the existing .xlsx
  #### Package Contents
  - `DataLogger.py` GUI 
  - `DataExport.py` non-GUI
  - `gui_add_ons/pbar.py`


## **Scripts: Misc.**
### `zillow.py` ***Current version*** --> v0.1.0 (beta) 
>Scraper is designed to aid in scraping rental properties in the zipcode of your choice and aggregates them into an Excel sheet for ease of distribution!

### `pbar_popup.py` ***Current version*** --> v1.1.1 
>ProgressBar is a module that displays a progress bar in a GUI application in response to user inputs and interactions with operating system(s) to open a file into the user's view. It also serves as a directory verifier to see if user inputs are correct. 

### `SpeedTest.py` ***Current version*** --> v4.2 🚧 🏗️ 🚧 --> TBD 
>SpeedTest is a standalone application that runs network speed test(s) with a data logging functionality. It allows for the user to complain about poor network performances via Twitter.  
  #### What's new? 
  - Standalone application in v4.2 
  
  #### What's to come? 
  - Adjustments to CSS selectors for composing and more consistent window handling in v4.2.1
  - Use configuration `.ini` files with `configparser` to parse, optimizations with context managers in v5.1

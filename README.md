# py_packages
>Contributor: Will

## 🐍 Contents 🐍 
### `DataLogger` ***Current version*** --> v2.1 
- Package for converting dataframes into an Excel file in its own directory 
- Default logging script for `SpeedTest.py` 
  #### What's new?
  - Dynamically adjust Excel file column width in v2.2 
  - Fix errors that cause .xlsx file to corrupt in v2.2 likely raised by MIME type of file  
  
  #### What's to come? 
  - Multi dataframe compiler method in v3.1
  - `contextmanager` to reduce potential errors from occurring in v3.1
     
### `SpeedTest` ***Current version*** --> v4.2 
- Package for running network speed(s) test with Twitter login functionality 
  #### What's new? 
  - Standalone application in v4.2 
  
  #### What's to come? 
  - Adjustments to CSS selectors for composing and more consistent window handling in v4.3
  - Use configuration `.ini` files with `configparser` to parse, optimizations with context managers in v5.1

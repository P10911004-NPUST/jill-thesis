# Jill-thesis
GUI for Jill-Tsai

## Suggestion:
Directly execute ***(pyenv) ..\python setup.py*** to install all required packages.

## Notation:
- The ***GDAL*** and ***Fiona*** packages could not be downloaded directly via ***pip install***. 
- They are currently downloaded with ***pipwin install***: pip install ***pipwin*** and ***wheel*** packages first.
- After the ***GDAL*** and ***Fiona*** were successfully installed, then pip install ***geopandas*** and ***rioxarray***, otherwise error might be raised, especially when installing ***geopandas***.

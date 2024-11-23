# PREREQUESITES:
- NodeJS (for server)
- Python (for client)


# DEPENDENCIES:
In `Project\Server`, open cmd/powershell, type `npm install` this will automatically install all dependencies  
In `Project\Client`, open cmd, type `pip install -r ..\requirements.txt`  


# RUN PROGRAMS:
In `Project\Server` type `node database`  
In `Project\Server` type `node grid`  
In `Project\Server` type `node index`  
In `Project\Client` type `py index.py`  
NOTE: currently, database and grid must be running before server (index)


# TROUBLESHOOTING:
## Check you have Node
in `Project\Server` type `node -v`  

## Check you have Python
in `Project\Client` type `python -V`  

## Check you have pip (should be installed with python}
In `Project\Client` type `pip -V`  
if you get an error, try `py -m pip -V`  
if that works, prefix any pip commands with `py -m`, otherwise install pip  

## Must run on python 3.10
In cmd or powershell, type `py -0`, if 3.10.x is not listed, install python 3.10  
If you have multiple versions of python, all python commands must be in the form `py -3.10 ...`
# PREREQUESITES:
- NodeJS (for server)
- Python (for client)


# DEPENDENCIES:
In `Project\Server`, open cmd/powershell, type
`npm install`  
this will automatically install all dependencies

In `Project\Client`, open cmd, type
`pip install -r .\requirements.txt`


# RUN PROGRAMS:
In `Project\Server` type `node index`
In `Project\Client` type `py index.py`  
-note- for now, the server needs to be run before the client, as the client assumes there is an existing server and will error if there isnt. This will be error handled in future, and wont be a problem.


# TROUBLESHOOTING:
## Check you have Node
in `Project\Server` type `node -v`

## Check you have Python
in `Project\Client` type `python -V`

## Check you have pip (should be installed with python}
In `Project\Client` type `pip -V`
if you get an error, try `py -m pip -V`
if that works, prefix any pip commands with `py -m`, otherwise, install pip using 
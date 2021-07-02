# InfoRadar

## Dependencies
Python version used: 3.9


### For downloading packages, run commands:
* conda install psycopg2
* conda install -c conda-forge cerberus
* conda install flask-restful
* conda install flask-sqlalchemy
* conda install -c conda-forge flask-marshmallow
* conda install marshmallow-sqlalchemy
* conda install -c conda-forge flup

## To run:
    pip install -e .
    (Windows) set FLASK_APP=inforadar
    (Linux) export FLASK_APP=inforadar
    flask run
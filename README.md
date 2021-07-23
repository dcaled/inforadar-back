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
* conda install -c conda-forge newspaper3k
* conda install pytorch torchvision torchaudio cpuonly -c pytorch
* conda install -c conda-forge transformers

## To run:
    pip install -e .
    (Windows) set FLASK_APP=inforadar
    (Linux) export FLASK_APP=inforadar
    flask run

## To upgrade on the server:
    git pull
    sudo systemctl restart inforadarapi.service 

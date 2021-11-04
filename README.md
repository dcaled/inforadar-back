# InfoRadar
InfoRadar - REST API.

## Installation

### External files
* Download and extract [CBOW 300 dimensions](http://143.107.183.175:22980/download.php?file=embeddings/word2vec/cbow_s300.zip) into `inforadar/lexica` folder. 

### Dependencies
* Python version: 3.9
* Anaconda version: 4.8.5

#### For downloading packages, run commands:
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
* conda install -c conda-forge pyspellchecker 

### Start the server
    pip install -e .
    (Windows) set FLASK_APP=inforadar
    (Linux) export FLASK_APP=inforadar
    flask run

### Update InfoRadar
    git pull
    sudo systemctl restart inforadarapi.service 

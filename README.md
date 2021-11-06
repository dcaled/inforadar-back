# InfoRadar
InfoRadar - REST API.

## Installation

### External files
* Download and extract [CBOW 300 dimensions](http://143.107.183.175:22980/download.php?file=embeddings/word2vec/cbow_s300.zip) into `inforadar/lexica` folder. 

### Dependencies
* Python version: 3.9
* Anaconda version: 4.8.5

Install the application dependencies:

    pip install -e .

### Start the server



Before starting the application, initiate the `multiprocessing.Manager` as a separate process.

    run python inforadar/word_embeddings_manager.py

From the Python documentation:
>Managers provide a way to create data which can be shared between different processes, including sharing over a network between processes running on different machines. A manager object controls a server process which manages shared objects. Other processes can access the shared objects by using proxies.

Then, start the server running flask:

    (Windows) set FLASK_APP=inforadar
    (Linux) export FLASK_APP=inforadar
    flask run

### Update InfoRadar
    git pull
    sudo systemctl restart inforadarapi.service 

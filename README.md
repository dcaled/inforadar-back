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

### Configure the server

We use a Gunicorn application server for the application, and Nginx to act as a front-end reverse proxy. The [guide](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04) shows how to configure and launch the application, creating a inforadarapi.service file.

### Start the server

Before starting the application, initiate the `multiprocessing.Manager` as a separate process.

    run python inforadar/word_embeddings_manager.py

From the Python documentation:
>Managers provide a way to create data which can be shared between different processes, including sharing over a network between processes running on different machines. A manager object controls a server process which manages shared objects. Other processes can access the shared objects by using proxies.

Then, start the server locally running flask:

    (Windows) set FLASK_APP=inforadar
    (Linux) export FLASK_APP=inforadar
    flask run

Or running the Gunicorn shown above.

### Update the server

When changes are made, whether remotely or locally, the server must be restarted.

    git pull
    sudo systemctl restart inforadarapi.service 

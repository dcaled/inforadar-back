from flask import Flask, g
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from gensim.models import KeyedVectors

import inforadar.db_data as db_data
from inforadar import constants

app = Flask(__name__)
# Configure the SqlAlchemy part of the app instance
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = db_data.postgres_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create the SqlAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)

print("Loading embedding matrix. This may take some time...")
word_embeddings_model = KeyedVectors.load_word2vec_format(constants.fp_emb_matrix,
                                                          binary=False,
                                                          limit=None)
print("Done loading embedding matrix.")

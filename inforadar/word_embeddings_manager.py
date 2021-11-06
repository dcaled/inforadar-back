import io
from multiprocessing.managers import BaseManager
import numpy as np
from gensim.models import KeyedVectors



def create_embedding_matrix(filepath, embedding_dim):
    print('Loading embeddings from disk...')
    embeddings = dict()
    with io.open(filepath, encoding='utf8') as f:
        for i, line in enumerate(f):
            if i == 0:
                continue
            if '00\u2009% 0.048951 -0.002307 0.021459 0.016691 -0.043448 -0.063223 -0.026633 0.037860 0.042934' in line:
                continue
            if '00\u2009% 0.003048 -0.021540 -0.010371 -0.037366 -0.004355 -0.055332 0.045417 -0.053561 0.038612' in line:
                continue
            word, *vector = line.split()
            try:
                embeddings[word] = np.array(vector, dtype=np.float32)[:embedding_dim]
            except Exception:
                pass
                # print(i, word, vector)

            if i == 10:
                return embeddings
    print('Done loading embeddings from disk...')
    return embeddings


def load_word_embeddings_model(filepath):
    print('Loading embeddings from disk...')
    word_embeddings_model = KeyedVectors.load_word2vec_format(
        filepath,
        binary=False,
        limit=None)
    print('Done loading embeddings from disk...')
    return word_embeddings_model


manager = BaseManager(address=('localhost', 5001), authkey=b'pass')
# manager.register('load_word_embeddings_model', load_word_embeddings_model)
manager.register('create_embedding_matrix', create_embedding_matrix)
server = manager.get_server()
server.serve_forever()

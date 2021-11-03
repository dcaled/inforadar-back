import json
import os

import inforadar.config as config
from inforadar.models import CorpusArticle, Category


def insert_article(article, category_id):
    corpus_article = CorpusArticle(
        category_id=category_id,
        source=article["source"],
        url=article["url"],
        headline=article["headline"],
        body_text=article["body_text"],
        top_image=article["top_image"],
        publish_date=article["publish_date"],
        filename=article["filename"]
    )

    config.db.session.add(corpus_article)
    config.db.session.commit()


def insert_collection(collection_path, category_id):
    sources = os.listdir(collection_path)
    for source in sources:
        source_path = "{}/{}".format(collection_path, source)
        files = os.listdir(source_path)
        for file in files:
            with open("{}/{}".format(source_path, file)) as data_file:
                article = json.load(data_file)
                if article["url"] == "":
                    article["url"] = None
                insert_article(article, category_id)


def main():
    data_path = "data_path"
    child_dirs = next(os.walk(data_path))[1]

    for collection in child_dirs:
        if collection == "hard news":
            collection_alias = "factual"
        elif collection == "soft news":
            collection_alias = "entertainment"
        # elif collection == "conspiracy":
        #    continue
        else:
            collection_alias = collection

        category_id = Category.query.filter_by(name=collection_alias).with_entities(Category.id).first()[0]

        collection_path = "{}/{}".format(data_path, collection)
        insert_collection(collection_path, category_id)


if __name__ == '__main__':
    main()

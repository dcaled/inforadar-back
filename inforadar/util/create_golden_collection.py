from inforadar.models import CorpusArticle
from sqlalchemy.sql.expression import func, select


def main():
    category_articles = {
        1: 30,  # hard news
        2: 30,  # opinion
        3: 30,  # soft news,
        4: 6,  # satire
        5: 7  # conspiracy
    }

    golden_collection = dict()

    for category_id, n_articles in category_articles.items():
        corpus_articles = CorpusArticle.query \
            .with_entities(CorpusArticle.id) \
            .filter(CorpusArticle.category_id == category_id) \
            .order_by(func.random()) \
            .limit(n_articles) \
            .all()

        # Filter outdated metrics.
        golden_collection[category_id] = [article.id for article in corpus_articles]

    print(golden_collection)

    golden_collection_set = set()
    for ids_by_category in golden_collection.values():
        ids_by_category = set(list(ids_by_category))
        golden_collection_set = golden_collection_set.union(ids_by_category)
    print(golden_collection_set)
    # print(len(golden_collection_set))


if __name__ == "__main__":
    main()

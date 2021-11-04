import numpy as np
import pandas as pd
from sqlalchemy import create_engine

import inforadar.db_data as db_data
from inforadar.models import Category, CorpusMetricScore, CorpusArticle


def jitter(a_series, noise_reduction=1000000):
    return (np.random.random(len(a_series)) * a_series.std() / noise_reduction) - (
            a_series.std() / (2 * noise_reduction))


def main():
    engine = create_engine(db_data.postgres_url)
    conn = engine.connect()

    metrics = {
        # 1: "sentiment",
        # 2: "subjectivity",
        # 3: "spell_checking",
        5: "headline_accuracy"
    }

    category_ids = Category.query.with_entities(Category.id)

    for category_id in category_ids:
        category_id = category_id[0]
        for metric_id in metrics.keys():
            records = CorpusMetricScore.query \
                .join(CorpusArticle, CorpusArticle.id == CorpusMetricScore.corpus_article_id) \
                .filter(CorpusMetricScore.metric_id == metric_id) \
                .filter(CorpusArticle.category_id == category_id) \
                .with_entities(
                    CorpusMetricScore.metric_id,
                    CorpusArticle.category_id,
                    CorpusMetricScore.id.label("corpus_metric_score_id"),
                    CorpusMetricScore.score)

            print(records)
            df = pd.read_sql(records.statement, records.session.bind)
            df['percentile'] = pd.qcut(df['score'] + jitter(df['score']), q=100, labels=False)

            print(df)
            df = df.drop(columns=['score'])
            df.to_sql(name='metrics_percentiles', con=engine, index=False, if_exists='append')


if __name__ == '__main__':
    main()

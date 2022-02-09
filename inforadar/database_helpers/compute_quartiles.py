import numpy as np

from inforadar.config import db
from inforadar.models import Category, CorpusMetricScore, MetricPercentile, CorpusMetricQuartile


def main():
    metrics = {
        # 1: "sentiment",
        # 2: "subjectivity",
        # 3: "spell_checking",
        4: "clickbait",
        # 5: "headline_accuracy",
    }

    quartiles = {
        "first_quartile": 25,
        "second_quartile": 50,
        "third_quartile": 75,
    }

    category_ids = Category.query.with_entities(Category.id)

    for category_id in category_ids:
        category_id = category_id[0]
        for metric_id in metrics.keys():
            cat_met_quartiles = {}
            for quartile in quartiles.keys():
                records = MetricPercentile.query \
                    .join(CorpusMetricScore, CorpusMetricScore.id == MetricPercentile.corpus_metric_score_id) \
                    .filter(CorpusMetricScore.metric_id == metric_id) \
                    .filter(MetricPercentile.category_id == category_id) \
                    .filter(MetricPercentile.percentile == quartiles[quartile]) \
                    .with_entities(CorpusMetricScore.score).all()
                cat_met_quartiles[quartile] = np.mean([record[0] for record in records])

            print(category_id, metric_id, cat_met_quartiles)
            CorpusMetricQuartile.query \
                .filter_by(metric_id=metric_id, category_id=category_id) \
                .update(cat_met_quartiles)
            db.session.commit()


if __name__ == '__main__':
    main()

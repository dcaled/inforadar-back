import sys

from cerberus import Validator
from flask import request
from flask_restful import Resource

import io
import pandas as pd
import numpy as np
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib import colors
from sqlalchemy.sql.expression import func
import inforadar.config as config
from inforadar.models import Category, Metric, CorpusMetricScore, CorpusArticle


class Histogram(Resource):
    def post(self):
        metrics_records = Metric.query.with_entities(
            Metric.id, Metric.name).all()
        available_metrics = {
            record.id: record.name for record in metrics_records}

        categories_records = Category.query.with_entities(
            Category.id, Category.name).all()
        categories = {record.id: record.name for record in categories_records}

        # --------------------------
        # Request validation.
        # --------------------------
        if not request.data:
            return {"message": f"Missing a JSON body in the request."}, 422

        allowed_schema = {
            "metrics": {"type": "list",
                        "required": True,
                        "allowed": available_metrics,
                        "schema": {"type": "integer"}
                        },
        }

        validator = Validator()
        valid = validator(request.get_json(force=True), allowed_schema)
        if not valid:
            return {"message": f"Unsupported json object: " + str(validator.errors)}, 400

        # --------------------------
        # Compute bins for each metric.
        # --------------------------
        data = request.get_json(force=True)
        metric_bins = dict()
        for metric_id in data.get("metrics"):
            if metric_id == 4:
                continue
            metric_bins[metric_id] = {"categories": dict()}
            for category_id in categories.keys():
                # Create the list of bins from our data
                pos_bins = config.db.session \
                    .query((func.floor(CorpusMetricScore.score / 0.001) * 0.001).label("floor"),
                           func.count(CorpusMetricScore.id).label("count")) \
                    .join(CorpusArticle, CorpusArticle.id == CorpusMetricScore.corpus_article_id) \
                    .filter(CorpusMetricScore.metric_id == metric_id) \
                    .filter(CorpusArticle.category_id == category_id) \
                    .group_by("floor") \
                    .order_by("floor")

                neg_bins = config.db.session \
                    .query((func.floor(CorpusMetricScore.score / 0.001) * 0.001).label("floor"),
                           func.count(CorpusMetricScore.id).label("count")) \
                    .join(CorpusArticle, CorpusArticle.id == CorpusMetricScore.corpus_article_id) \
                    .filter(CorpusMetricScore.metric_id == metric_id) \
                    .filter(CorpusArticle.category_id != category_id) \
                    .group_by("floor") \
                    .order_by("floor")

                bins = config.db.session \
                    .query(CorpusMetricScore.score, CorpusArticle.category_id, CorpusMetricScore.metric_id) \
                    .join(CorpusArticle, CorpusArticle.id == CorpusMetricScore.corpus_article_id) \
                    .filter(CorpusMetricScore.metric_id == metric_id) \
                    .order_by(CorpusMetricScore.score)

                df = pd.read_sql(bins.statement, bins.session.bind)
                df['categoria'] = np.where(
                    df['category_id'] == category_id, f'categoria {category_id}', 'outras')
                sns.set_theme(style="whitegrid")
                plt.rcParams['axes.spines.right'] = False
                plt.rcParams['axes.spines.left'] = False
                plt.rcParams['axes.spines.top'] = False
                plt.rcParams['axes.grid.axis'] = 'y'
                plt.rcParams['figure.figsize'] = [4, 3]
                plt.rcParams['svg.fonttype'] = 'none'
                plt.rcParams['text.color'] = plt.rcParams['xtick.color'] = plt.rcParams['ytick.color'] = 'grey'

                hist = sns.histplot(data=df, x="score",
                                    hue="categoria", palette=['#00539d', '#8c8c8c'], bins=25, hue_order=[f'categoria {category_id}', "outras"])
                hist.plot()

                for patch in hist.patches:
                    if patch.get_x() <= 0.05 < patch.get_x() + patch.get_width() and colors.to_hex(patch.get_facecolor()) == '#00539d':
                        patch.set_facecolor('#f4664a')

                a = stats.ks_2samp(df.loc[df['category_id'] == category_id]['score'],
                                   df.loc[df['category_id'] != category_id]['score'])
                plt.suptitle(
                    f'{round(a.statistic, 3)}, p={round(a.pvalue, 5)}')
                plotoutput = io.StringIO()
                plt.savefig(plotoutput, format='svg')
                plt.close()
                #f = open(f'c{category_id}m{metric_id}.svg', 'w')
                # f.write(plotoutput.getvalue())
                # f.close()

                # select
                #   floor(actions_count/100.00)*100 as bin_floor,
                #   count(user_id) as count
                # from product_actions
                # group by bin_floor
                # order by bin_floor;

                metric_bin_pos = []
                metric_bin_neg = []
                for b in pos_bins.all():
                    metric_bin_pos.append({
                        "count": b.count,
                        "value": b.floor
                    })
                for b in neg_bins.all():
                    metric_bin_neg.append({
                        "count": b.count,
                        "value": b.floor
                    })
                metric_bins[metric_id]["categories"][category_id] = {
                    "pos": metric_bin_pos, "neg": metric_bin_neg, "svg": plotoutput.getvalue()}
                plotoutput.close()

        return metric_bins, 200

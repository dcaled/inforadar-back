import sys
import json

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
import inforadar.config as config
from inforadar.models import Category, Metric, CorpusMetricScore, CorpusArticle
from ..constants import cache_histograms


class Histogram(Resource):
    def post(self):
        metrics_records = Metric.query.with_entities(
            Metric.id, Metric.name).all()
        available_metrics = {
            record.id: record.name for record in metrics_records}

        categories_records = Category.query.with_entities(
            Category.id, Category.display_name).all()
        categories = {
            record.id: record.display_name.lower() for record in categories_records}

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
            "metric_scores": {"type": "dict",
                              "required": False,
                              "keysrules": {
                                  "type": "string",
                                  "allowed": [str(m) for m in available_metrics],
                              },
                              "valuesrules": {"type": "dict",
                                              "schema": {
                                                  "score": {"type": "float"}}
                                              },
                              },
            "settings": {"type": "dict",
                         "required": True,
                         "schema": {
                             "graphs": {"type": "list",
                                        "required": True,
                                        "allowed": ["count", "cumulative", "notcumulative"],
                                        "schema": {"type": "string"}
                                        },
                             "legend": {"type": "boolean",
                                        "required": True,
                                        }},
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
        metric_scores = data.get("metric_scores")
        legend = data.get("settings")["legend"]
        graphs = data.get("settings")["graphs"]
        histocache = False

        if (not metric_scores):
            try:
                f = open(cache_histograms, 'r')
                histocache = json.load(f)
                f.close()
            except FileNotFoundError:
                histocache = False

        for metric_id in data.get("metrics"):
            if (histocache):
                break

            metric_bins[metric_id] = {"categories": dict()}
            for category_id in categories.keys():
                # Filter our data
                metricdata = config.db.session \
                    .query(CorpusMetricScore.score, CorpusArticle.category_id, CorpusMetricScore.metric_id) \
                    .join(CorpusArticle, CorpusArticle.id == CorpusMetricScore.corpus_article_id) \
                    .filter(CorpusMetricScore.metric_id == metric_id) \
                    .order_by(CorpusMetricScore.score)

                df = pd.read_sql(metricdata.statement, metricdata.session.bind)
                df['coleção'] = np.where(
                    df['category_id'] == category_id, categories[category_id], 'restantes')
                sns.set_theme(style="whitegrid")
                plt.rcParams['axes.spines.right'] = False
                plt.rcParams['axes.spines.left'] = False
                plt.rcParams['axes.spines.top'] = False
                plt.rcParams['axes.grid.axis'] = 'y'
                plt.rcParams['figure.figsize'] = [4, 3]
                plt.rcParams['svg.fonttype'] = 'none'
                plt.rcParams['text.color'] = plt.rcParams['xtick.color'] = plt.rcParams[
                    'ytick.color'] = plt.rcParams['axes.labelcolor'] = 'grey'

                article_color = '#f4664a'
                collection_color = '#00539d'
                others_color = '#8c8c8c'
                palette = ([article_color]
                           if metric_scores else []) + [collection_color, others_color]
                hue_order = (["artigo"]
                             if metric_scores else []) + [categories[category_id], "restantes"]

                plotoutput_nc = io.StringIO()
                plotoutput_c = io.StringIO()
                plotoutput_ct = io.StringIO()

                if ("notcumulative" in graphs):
                    hist_nc = sns.histplot(data=df, x="score", cumulative=False, common_norm=False, stat="probability",
                                           legend=legend, hue="coleção", palette=palette, bins=25, hue_order=hue_order)
                    hist_nc.plot()

                    if (metric_scores):
                        for patch in hist_nc.patches:
                            if patch.get_x() <= metric_scores[str(metric_id)]['score'] < patch.get_x() + patch.get_width() and colors.to_hex(patch.get_facecolor()) == collection_color:
                                patch.set_facecolor(article_color)
                    plt.xlabel('pontuação')
                    plt.ylabel('probabilidade')
                    plt.savefig(plotoutput_nc, format='svg',
                                bbox_inches='tight')
                    plt.close()

                if ("cumulative" in graphs):
                    hist_c = sns.histplot(data=df, x="score", cumulative=True, common_norm=False, stat="probability",
                                          legend=legend, hue="coleção", palette=palette, bins=25, hue_order=hue_order)
                    hist_c.plot()

                    if (metric_scores):
                        for patch in hist_c.patches:
                            if patch.get_x() <= metric_scores[str(metric_id)]['score'] < patch.get_x() + patch.get_width() and colors.to_hex(patch.get_facecolor()) == collection_color:
                                patch.set_facecolor(article_color)
                    plt.xlabel('pontuação')
                    plt.ylabel('probabilidade acumulada')
                    plt.savefig(plotoutput_c, format='svg',
                                bbox_inches='tight')
                    plt.close()

                if ("count" in graphs):
                    hist_ct = sns.histplot(data=df, x="score", cumulative=False, common_norm=True, stat="count",
                                           legend=legend, hue="coleção", palette=palette, bins=25, hue_order=hue_order)
                    hist_ct.plot()

                    if (metric_scores):
                        for patch in hist_ct.patches:
                            if patch.get_x() <= metric_scores[str(metric_id)]['score'] < patch.get_x() + patch.get_width() and colors.to_hex(patch.get_facecolor()) == collection_color:
                                patch.set_facecolor(article_color)
                    plt.xlabel('pontuação')
                    plt.ylabel('nº de artigos')
                    plt.savefig(plotoutput_ct, format='svg',
                                bbox_inches='tight')
                    plt.close()

                dfrange_samecat = df.loc[df['category_id'] == category_id]
                dfrange_notsamecat = df.loc[df['category_id'] != category_id]
                if (len(dfrange_samecat) and len(dfrange_notsamecat)):
                    ks = stats.ks_2samp(
                        dfrange_samecat['score'], dfrange_notsamecat['score'])

                metric_bins[metric_id]["categories"][category_id] = {
                    "svg": {"notcumulative": plotoutput_nc.getvalue(), "cumulative": plotoutput_c.getvalue(), "count": plotoutput_ct.getvalue()}, "ks_2samp": {"stat": ks.statistic, "p": ks.pvalue}}
                plotoutput_nc.close()
                plotoutput_c.close()
                plotoutput_ct.close()

        if (not metric_scores):
            if (not histocache):
                f = open(cache_histograms, 'w')
                json.dump(metric_bins, f)
                f.close()
            else:
                metric_bins = histocache

        return metric_bins, 200

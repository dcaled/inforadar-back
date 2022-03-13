-- Add version to corpus_metrics_scores table.
ALTER TABLE corpus_metrics_scores DROP CONSTRAINT corpus_metrics_scores_corpus_article_id_metric_id_key;

ALTER TABLE corpus_metrics_scores
    ADD CONSTRAINT corpus_ms_crp_art_id_met_id_version_key
    UNIQUE(corpus_article_id, metric_id, version);


-- Add version to crowdsourced_metrics_scores table.
ALTER TABLE crowdsourced_metrics_scores DROP CONSTRAINT crowdsourced_metrics_scores_metric_id_crowdsourced_article__key;

ALTER TABLE crowdsourced_metrics_scores
    ADD CONSTRAINT crowdsourced_ms_crd_art_id_met_id_version_key
    UNIQUE(crowdsourced_article_id, metric_id, version);


-- Add version to corpus_indicators_scores table.
ALTER TABLE corpus_indicators_scores DROP CONSTRAINT corpus_indicators_scores_corpus_article_id_indicator_id_key;

ALTER TABLE corpus_indicators_scores
    ADD CONSTRAINT corpus_is_crp_art_id_ind_id_version_key
    UNIQUE(corpus_article_id, indicator_id, version);

-- Add version to crowdsourced_indicators_scores table.
ALTER TABLE crowdsourced_indicators_scores DROP CONSTRAINT crowdsourced_indicators_score_indicator_id_crowdsourced_art_key;

ALTER TABLE crowdsourced_indicators_scores
    ADD CONSTRAINT crowdsourced_is_crd_art_id_ind_id_cat_id_version_key
    UNIQUE(crowdsourced_article_id, indicator_id, category_id, version);


-- Add version to metrics_percentiles table.
ALTER TABLE metrics_percentiles ADD COLUMN version INTEGER DEFAULT 1 NOT NULL;

ALTER TABLE metrics_percentiles DROP CONSTRAINT metrics_percentiles_metric_id_category_id_corpus_metric_sco_key;

ALTER TABLE metrics_percentiles
    ADD CONSTRAINT metrics_percentiles_met_id_cat_id_crp_ms_version_key
    UNIQUE(metric_id, category_id, corpus_metric_score_id, version);

-- Add version to indicators_percentiles table.

ALTER TABLE indicators_percentiles ADD COLUMN version INTEGER DEFAULT 1 NOT NULL;

ALTER TABLE indicators_percentiles DROP CONSTRAINT indicators_percentiles_indicator_id_category_id_corpus_indi_key;

ALTER TABLE indicators_percentiles
    ADD CONSTRAINT indicators_percentiles_ind_id_cat_id_crp_is_version_key
    UNIQUE(indicator_id, category_id, corpus_indicator_score_id, version);


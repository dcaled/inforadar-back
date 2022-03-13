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
#!/usr/bin/env python
# -*- coding: utf-8 -*-

############################################
# File path to lexica.
############################################

base_dir = "inforadar/lexica/"

# ANEW lexica
# fp_lex_raw_anew = '{}anew-pt.csv'.format(base_dir)
# fp_lex_raw_anew_extended = '{}BRM-emot-submit-pt.csv'.format(base_dir)
# fp_lex_anew = '{}processed\\anew.pkl'.format(base_dir)

# Emotion lexica
# fp_lex_raw_emotion = '{}emotions'.format(base_dir)
# fp_lex_emotion = '{}processed\\emotion.pkl'.format(base_dir)

# LIWC lexicon
# fp_lex_raw_liwc = '{}LIWC2007_Portugues_win.dic.txt'.format(base_dir)
# fp_lex_liwc = '{}processed\\liwc.pkl'.format(base_dir)

# Sentiment lexica
fp_lex_raw_sent_sentilex = "{}SentiLex-flex-PT02.txt".format(base_dir)
# fp_lex_raw_oplexicon = '{}oplexico_v3.0.txt'.format(base_dir)
fp_lex_sent = "{}processed/sentiment.pkl".format(base_dir)

# Subjectivity lexicon
# fp_lex_raw_subj = '{}subjectivity-clues-pt.csv'.format(base_dir)
fp_lex_subj = "{}processed/subjectivity.pkl".format(base_dir)

# Embeddings path
fp_emb_matrix = "{}cbow_s300.txt".format(base_dir)

# Explainable rules
fp_explainable_rules = "inforadar/util/explainable_rules.json"

# Clickbait models
fp_clickbait_vectorizer = "inforadar/util/clickbait_vectorizer.pk"
fp_clickbait_model = "inforadar/util/clickbait_model.sav"

# Histograms cache
cache_histograms = "inforadar/util/histocache.json"

# Indicators current version
current_version_indicator_1 = 1

# Metrics current version
current_version_metric_clickbait = 1
current_version_metric_sentiment = 1
current_version_metric_subjectivity = 1
current_version_metric_spell_checking = 1
current_version_metric_headline_accuracy = 1

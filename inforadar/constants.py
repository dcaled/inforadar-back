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

# Extended vocabulary
fp_extended_vocabulary = "{}extended_vocabulary_20.pkl".format(base_dir)

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
metrics_current_version = {
    "sentiment": 1,
    "subjectivity": 1,
    "spell_checking": 2,
    "headline_accuracy": 1,
    "clickbait": 1
}

# Articles to be annotated by journalists.
golden_collection_by_category_journalists = {
    1: [5950, 5892, 6286, 6304, 4681, 6070, 2648, 1652, 6229, 2356, 6118, 2859, 5762, 1847, 6066, 3441, 5316, 4684,
        6368, 7003, 6905, 6592, 5077, 4127, 3289, 4104, 1769, 4590, 3188, 6406],
    2: [10596, 11618, 12354, 10242, 8696, 8557, 11944, 10764, 10675, 10295, 11525, 10670, 12549, 12707, 12073, 10109,
        8429, 7370, 10582, 9640, 10656, 8641, 12369, 10842, 13158, 8316, 10085, 9498, 12800, 10258],
    3: [15943, 17333, 16642, 18633, 19012, 18078, 17663, 15650, 14702, 19693, 16464, 17760, 14302, 14464, 16066, 19701,
        19146, 16738, 14732, 15689, 14667, 19015, 16663, 16793, 15659, 14318, 18978, 14574, 16369, 17445],
    4: [13583, 13314, 13698, 13342, 13954, 13276],
    5: [91, 257, 158, 819, 44, 370, 1093]}

# Articles to be annotated by hired annotators.
golden_collection_by_category_hired = {
    1: [4684, 6070, 5077, 6905, 6592, 4127, 4681, 5762, 4590, 5950, 2648, 5892, 3188, 6406, 3289, 6286, 2859, 6304,
        1652, 5316],
    2: [10295, 8429, 10656, 7370, 12800, 11525, 10764, 12369, 10596, 9498, 10582, 10109, 12354, 13158, 10675, 10085,
        8557, 10670, 11618, 8696],
    3: [19012, 16663, 14302, 19701, 17445, 14667, 15943, 16642, 18633, 18078, 17333, 16066, 17663, 14574, 15650, 14702,
        19146, 14464, 14318, 16464],
    4: [13583, 13314, 13698, 13342, 13954, 13276, 13336, 14012, 14174, 13729, 13662, 13933, 14063, 13761, 13352, 13519,
        13824, 14189, 13617, 13975],
    5: [91, 257, 158, 819, 44, 370, 1093, 921, 122, 563, 559, 30, 1111, 768, 522, 556, 984, 26, 929, 770]}

# golden_collection_ids = set(range(1, 10))
# golden_collection_ids = {12800, 257, 10242, 16642, 5892, 11525, 6406, 12549, 4104, 13314, 10764, 13583, 10258, 16663,
#                         9498, 13342, 4127, 15650, 18978, 17445, 12073, 2859, 15659, 44, 819, 2356, 1847, 10295, 5950,
#                         12354, 19012, 1093, 15943, 19015, 4681, 15689, 14667, 4684, 16464, 12369, 6229, 10582, 2648,
#                         10842, 7003, 91, 17760, 11618, 16738, 10596, 10085, 13158, 8557, 14702, 3441, 370, 1652, 3188,
#                         8316, 10109, 14464, 5762, 13698, 13954, 14732, 6286, 16793, 18078, 158, 6304, 10656, 12707,
#                         11944, 9640, 10670, 6066, 10675, 17333, 6070, 6592, 8641, 16066, 5316, 18633, 7370, 19146,
#                         5077, 3289, 13276, 14302, 6368, 6118, 1769, 8429, 4590, 19693, 14318, 14574, 16369, 19701,
#                         8696, 6905, 17663}


golden_collection_ids = {12800, 13824, 16642, 13314, 5892, 11525, 6406, 257, 770, 522, 10764, 13583, 16663, 13336, 9498,
                         26, 13342, 4127, 30, 15650, 17445, 13352, 2859, 44, 556, 559, 13617, 819, 563, 10295, 5950,
                         12354, 19012, 1093, 15943, 4681, 14667, 4684, 16464, 12369, 10582, 1111, 2648, 91, 13662,
                         14174, 11618, 10596, 10085, 13158, 8557, 14702, 13933, 14189, 370, 3188, 1652, 122, 10109,
                         14464, 5762, 13698, 13954, 6286, 13975, 921, 18078, 158, 6304, 10656, 13729, 929, 10670, 10675,
                         17333, 6070, 14012, 6592, 13761, 16066, 5316, 18633, 7370, 19146, 13519, 5077, 984, 3289,
                         13276, 14302, 8429, 4590, 14574, 14318, 14063, 19701, 8696, 6905, 768, 17663}

demo_ids = {11, 4000, 7000, 9000, 10000, 11000, 13000, 15000, 19002}

article_collections_strings = {
    0: "default",
    1: "mint",
    2: "main",
    3: "lusa",
    4: "demo",
}

article_collections = {
    0: golden_collection_ids,
    1: golden_collection_ids,
    2: golden_collection_ids,
    3: golden_collection_ids,
    4: demo_ids,
}

annotation_reply = {
    "MINT": 1,
    "MAIN": 2,
}

article_collection_to_reply = {
    0: annotation_reply["MINT"],
    1: annotation_reply["MINT"],
    2: annotation_reply["MAIN"],
    3: annotation_reply["MINT"],
    4: annotation_reply["MINT"],
}

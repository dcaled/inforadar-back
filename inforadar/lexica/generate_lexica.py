import pickle

from inforadar.credibility_metrics.sentiment_metric import SentimentMetric
from inforadar.constants import fp_lex_raw_sent_sentilex, fp_lex_sent


def main():
    sentiment_metric = SentimentMetric()
    sentilex = sentiment_metric.create_sentilex(fp_lex_raw_sent_sentilex)
    # print(sentilex)

    with open("../lexica/processed/sentiment.pkl", 'wb') as f:
        pickle.dump(sentilex, f)
    print('Done Sentilex.')


if __name__ == "__main__":
    main()

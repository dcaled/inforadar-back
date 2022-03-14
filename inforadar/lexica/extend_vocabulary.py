import os
import json
import pickle
from tqdm import tqdm
from spellchecker import SpellChecker
from inforadar.article import Article


def load_article(filepath):
    with open(filepath, encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


def search_frequent_unknown_words(source_path):
    files = os.listdir(source_path)
    all_unknown_words = dict()
    # Iterate over files.
    for filename in tqdm(files):
        # Load json file.
        data = load_article('{}/{}'.format(source_path, filename))
        article = Article(headline=data['title'], body=data['text'])

        unknown_words = check_unknown_words(article.headline_as_list + article.body_as_list)
        for word in unknown_words:
            all_unknown_words[word] = all_unknown_words.get(word, 0) + 1
    return all_unknown_words


def check_unknown_words(text_as_list):
    spell_portuguese = SpellChecker(language="pt")
    misspelled = spell_portuguese.unknown(text_as_list)
    return misspelled


def main():
    path_to_lusa_data = "path_to_lusa_dataset"
    path_to_words_list_freq_1 = "/inforadar/lexica/extended_vocabulary_1.pkl"
    path_to_words_list_freq_5 = "/inforadar/lexica/extended_vocabulary_5.pkl"
    path_to_words_list_freq_10 = "/inforadar/lexica/extended_vocabulary_10.pkl"
    path_to_words_list_freq_15 = "/inforadar/lexica/extended_vocabulary_15.pkl"
    path_to_words_list_freq_20 = "/inforadar/lexica/extended_vocabulary_20.pkl"

    unknown_words = search_frequent_unknown_words(path_to_lusa_data)
    # unknown_words_freq_5 = {k: v for k, v in unknown_words.items() if v >= 5}
    # unknown_words_freq_10 = {k: v for k, v in unknown_words.items() if v >= 10}
    # unknown_words_freq_15 = {k: v for k, v in unknown_words.items() if v >= 15}
    unknown_words_freq_20 = {k: v for k, v in unknown_words.items() if v >= 20}

    # print(unknown_words)
    # print(selected_words)
    # print(sorted(list(selected_words.keys())))
    # print(len(unknown_words))
    # print(len(selected_words))

    # pickle.dump(unknown_words, open(path_to_words_list_freq_1, "wb"))
    # pickle.dump(unknown_words_freq_5, open(path_to_words_list_freq_5, "wb"))
    # pickle.dump(unknown_words_freq_10, open(path_to_words_list_freq_10, "wb"))
    # pickle.dump(unknown_words_freq_15, open(path_to_words_list_freq_15, "wb"))
    # pickle.dump(unknown_words_freq_20, open(path_to_words_list_freq_20, "wb"))

    # unknown_words_loaded = pickle.load(open(path_to_words_list_freq_10, "rb"))
    # unknown_words_freq_15 = pickle.load(open(path_to_words_list_freq_15, "rb"))
    unknown_words_freq_20 = pickle.load(open(path_to_words_list_freq_20, "rb"))

    # print(len(unknown_words_loaded))
    # print(len(unknown_words_freq_15))
    print(unknown_words_freq_20)
    print(len(unknown_words_freq_20))


if __name__ == '__main__':
    main()

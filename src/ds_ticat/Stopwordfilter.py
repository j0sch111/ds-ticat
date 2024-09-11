import re

import yaml


class Stopwordfilter:
    def load_stopwords_pattern(stop_words_file, key_name):
        """
        Load stopwords from yaml file.
        """
        with open(stop_words_file, "r", encoding="utf-8") as file:
            stop_words_data = yaml.safe_load(file)
        stop_words = set(map(str.lower, stop_words_data[keyname]))
        stop_words_pattern = r"\b(?:" + "|".join(map(re.escape, stop_words)) + r")\b"

        return stop_words_pattern

    def remove_stop_words(text, greetings_file, key_name):
        """
        Removes stop words from the text.
        """
        stop_words_pattern = load_stopwords_pattern()

        words_list = text.split()
        filtered_words = [word for word in words_list if word.lower() not in stop_words_pattern]
        text = " ".join(filtered_words)
        return text

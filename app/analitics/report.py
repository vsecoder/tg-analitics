import re
import string

import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords

import pandas as pd
from ydata_profiling import ProfileReport

nltk.download('punkt')
nltk.download('stopwords')


def get_report(chats):
    """
    Get report

    :param chats: chats from result.json
    :return:
    """
    result_array = []
    for chat in chats:
        messages = chat['messages']
        for message in messages:
            try:
                if message['from_id'] != "user1218845111":
                    continue
            except KeyError:
                continue
            text = message['text']
            if type(text) is not str:
                text = ""
                for item in message['text']:
                    text += str(item['text']) if type(item) is dict else str(item)
            result_array.append(text.replace("\n", " "))

    result_str = " ".join(result_array).lower()
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002500-\U00002BEF"  # chinese char
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001f926-\U0001f937"
        "\U00010000-\U0010ffff"
        "\u2640-\u2642"
        "\u2600-\u2B55"
        "\u200d"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\ufe0f"  # dingbats
        "\u3030"
        "]+",
        re.UNICODE,
    )
    emojies = re.findall(emoji_pattern, result_str)
    result_str = emoji_pattern.sub(r"", result_str)
    punctuations = re.findall(r"[^\s\w]", result_str)
    result_str = result_str.translate(str.maketrans("", "", string.punctuation))
    text_tokens = word_tokenize(result_str)
    russian_stopwords = stopwords.words("russian")
    russian_stopwords.extend([str(i) for i in range(0, 101)])
    russian_stopwords.extend(["—", "«", "»", "•", "ℹ️", "abragadabraa"])

    text_tokens = [token.strip() for token in text_tokens if token not in russian_stopwords]

    # report words
    ProfileReport(
        pd.DataFrame(data=text_tokens, columns=["words"]), title="Report words"
    ).to_file("output/report_words.html")

    # report emojis
    ProfileReport(
        pd.DataFrame(data=emojies, columns=["emojies"]), title="Report emojis"
    ).to_file("output/report_emojis.html")

    # report punctuation
    ProfileReport(
        pd.DataFrame(data=punctuations, columns=["punctuations"]),
        title="Report punctuations",
    ).to_file("output/report_punctuation.html")

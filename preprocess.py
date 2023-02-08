# import nltk
from pymystem3 import Mystem
from string import punctuation
from nltk.corpus import stopwords
from razdel import sentenize, tokenize
from tqdm import tqdm

# nltk.download("stopwords")
punctuation += "«»— 1234567890"
rus_stopwords = stopwords.words("russian")
rus_stopwords.extend(["весь", "владимир", "com", "джо", "m", "михаил", "оба", ""])
mystem = Mystem()


def tokenize_test(sentence):
    tokens = [token.text.lower() for token in tokenize(sentence)]
    tokens = [token for token in tokens if token not in rus_stopwords
              and not set(token).intersection(punctuation)]
    return " ".join(tokens).strip()


def preprocess_text(doc):
    new_sent = tokenize_test(doc)
    tokens = mystem.lemmatize(new_sent)
    tokens = [token for token in tokens if token != " "
              and token not in rus_stopwords]
    text = " ".join(tokens)
    return text


def lemmatize_doc(sentences, filename):
    doc_split = []
    buf = []
    test = preprocess_text(' ‽ '.join(sentences))
    for x in tqdm(test.split(' ')):
        if '‽' in x:
            doc_split += [' '.join(buf) + "\n"]
            buf = []
        else:
            buf += [x]
    doc_split += [' '.join(buf)]
    with open(f"data/{filename}_lemmatized.txt", "w", encoding="utf-8") as f:
        f.writelines(doc_split)


def main():
    medias = ["lenta", "tvRain"]
    for media in medias:
        with open(f"data/data_{media}.txt", "r", encoding="utf-8") as f:
            text = f.readlines()
        sentences = []
        for line in text:
            article_sentences = [sent.text for sent in list(sentenize(line))
                                 if sent.text != "\n"]
            sentences.extend(article_sentences)
        lemmatize_doc(sentences, media)


if __name__ == "__main__":
    main()

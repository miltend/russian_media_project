# import nltk
from pymystem3 import Mystem
from string import punctuation
from nltk.corpus import stopwords
from razdel import sentenize, tokenize
from tqdm import tqdm

# nltk.download("stopwords")

punctuation += "«»— 1234567890"
rus_stopwords = stopwords.words("russian")
mystem = Mystem()


def tokenize_test(sentence):
    tokens = [token.text.lower() for token in tokenize(sentence)]
    tokens = [token for token in tokens if token not in rus_stopwords
              and not set(token).intersection(punctuation)]
    return " ".join(tokens).strip()


def preprocess_text(doc):
    new_sent = tokenize_test(doc)
    tokens = mystem.lemmatize(new_sent)
    tokens = [token for token in tokens if token != " "]
    text = " ".join(tokens)
    return text

with open("data_lenta.txt", "r", encoding="utf-8") as f:
    text = f.readlines()

with open("sentenized.txt", "w", encoding="utf-8") as f:
    for line in tqdm(text):
        sentences = [sent.text for sent in list(sentenize(line))]
        for sentence in sentences:
            if sentence:
                f.write(sentence + "\n")


with open("sentenized.txt", "r", encoding="utf-8") as f:
    new_text = f.readlines()
doc_split = []
buf = []
test = preprocess_text(' ‽ '.join(new_text))

for x in tqdm(test.split(' ')):
    if '‽' in x:
        doc_split += [' '.join(buf) + "\n"]
        buf = []
    else:
        buf += [x]
doc_split += [' '.join(buf)]
with open("lenta_lemmatized.txt", "w", encoding="utf-8") as f:
    f.writelines(doc_split)


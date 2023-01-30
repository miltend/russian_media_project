# import nltk
from pymystem3 import Mystem
from string import punctuation
from nltk.corpus import stopwords
from razdel import sentenize, tokenize
from tqdm import tqdm

# nltk.download("stopwords")

punctuation += "«»— "
rus_stopwords = stopwords.words("russian")
mystem = Mystem()


def lemmatize(sentence):
    tokens = " ".join([token.text.lower() for token in tokenize(sentence)]).strip()
    lemmas = mystem.lemmatize(tokens)
    lemmas = [lemma for lemma in lemmas if lemma not in rus_stopwords
              and not set(lemma).intersection(punctuation)]
    return lemmas


with open("data_lenta.csv", "r", encoding="utf-8") as f:
    text = f.readlines()


# with open("lenta_lem.txt", "w", encoding="utf-8") as f:
#     for line in tqdm(text):
#         sentences = [sent.text for sent in list(sentenize(line))]
#         for sentence in sentences:
#             if sentence:
#                 lemmas = lemmatize(sentence)
#                 # print(lemmas)
#                 f.write(" ".join(lemmas).strip() + "\n")

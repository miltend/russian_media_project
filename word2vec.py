import gensim
from gensim.models import word2vec
from tqdm import tqdm
import time


data = word2vec.LineSentence("lenta_lem.txt")
model = gensim.models.Word2Vec(data, vector_size=300, window=5, min_count=2, workers=2)
model.save("word2vec.model")

model = gensim.models.Word2Vec.load("word2vec.model")

words = ["Россия", "Украина", "Путин", "Европа", "Зеленский"]



word = "путин"

print(len(model.wv))

for word in words:
    print(word, "\n")
    for neighbour in model.wv.most_similar(word.lower(), topn=20):
        print(neighbour)
    print("\n")
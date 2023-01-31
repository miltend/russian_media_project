import gensim
from gensim.models import word2vec

data = word2vec.LineSentence("lenta_lemmatized.txt")
model = gensim.models.Word2Vec(data, vector_size=300, window=2, min_count=2, workers=2, sg=1)
model.save("word2vec.model")

model = gensim.models.Word2Vec.load("word2vec.model")

words = ["Россия", "Украина", "Путин", "Европа", "Запад", "Зеленский", "война", "сво", "украинец"]

# words = [""]

# print(len(model.wv))

for word in words:
    print(word, "\n")
    for neighbour in model.wv.most_similar(word.lower(), topn=10):
        print(neighbour)
    print("\n")
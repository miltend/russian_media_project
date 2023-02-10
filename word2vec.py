import gensim
from gensim.models import word2vec

medias = ["lenta", "tvRain"]
for media in medias:
    data = word2vec.LineSentence(f"data/{media}_lemmatized.txt")
    model = gensim.models.Word2Vec(data, vector_size=200, window=12, min_count=2, workers=2, sg=1)
    model.save(f"models/word2vec_{media}.model")


words = ["Россия", "Украина", "Путин", "Европа", "Зеленский"]

model_lenta = gensim.models.Word2Vec.load("models/word2vec_lenta.model")
model_tvrain = gensim.models.Word2Vec.load("models/word2vec_tvrain.model")


for word in words:
    print(word, "\n")
    neighbours_lenta = model_lenta.wv.most_similar(word.lower(), topn=10)
    neighbours_tvrain = model_tvrain.wv.most_similar(word.lower(), topn=10)
    for i in range(10):
        print(neighbours_lenta[i], "\t\t\t\t", neighbours_tvrain[i])
    print("\n")

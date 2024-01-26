from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
import nltk
# nltk.download('punkt')

# Sample corpus
corpus = ["Your text data here. It could be a single string or a list of strings.",
          "Your text data here. It could be a single "]

# Tokenization
tokens = [word_tokenize(doc.lower()) for doc in corpus]

# Training the Word2Vec model
model = Word2Vec(sentences=tokens, vector_size=100, window=5, min_count=1, workers=4)

# Accessing the word vector for a specific word
word_vector = model.wv['could']

# Finding similar words
similar_words = model.wv.most_similar('could')
print(similar_words)

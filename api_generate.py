# please run this file to generate the glove model before running the main.py file
import gensim.downloader as api

word_vectors = api.load("glove-wiki-gigaword-100")
word_vectors.save("./working/glove-wiki-gigaword-100.model")
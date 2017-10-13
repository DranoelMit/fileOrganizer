import os
import nltk
import gensim
from gensim import corpora, models, similarities


model = gensim.models.Word2Vec.load('C:/Users/Tim/Desktop/Projects/fileOrganizer/AI')

keyword = input("Enter a word to find relatives: ")
print(str(model.most_similar(keyword)))

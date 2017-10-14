import os
import nltk
import gensim
from gensim import corpora, models, similarities

folderPath = input("Enter a word to find relatives: ")
fileOrganizer(folderPath)


def fileOrganizer(path):
    #model = gensim.models.Word2Vec.load(os.getcwd()+"/AI")
#print(str(model.most_similar(keyword)))

import os
import nltk
import gensim
from gensim import corpora, models, similarities

tok_corp=[]

os.chdir('corpus')
for filename in os.listdir(os.getcwd()):
    df = open(filename,'r', errors='replace')

    corpus = df.readlines()

    for sent in corpus:
        tok_corp += [nltk.word_tokenize(sent)]

model = gensim.models.Word2Vec(tok_corp, min_count=1, size = 32)


#print(str(model.most_similar('dog')))
model.save('C:/Users/Tim/Desktop/Projects/fileOrganizer/AI')

import os
import nltk
import gensim
from fold import makeFolder, placeInFolder
from gensim import corpora, models, similarities
from rake_nltk import Rake


folderPath = input("Enter the path you would like to organize: ")
keywordDict ={}

def fileOrganizer(path):
    #Stage 1.0: find keywords in each file
    for filename in os.listdir(path):
        if(filename[filename.rfind('.'):] != '.txt'):
            print("ERROR: the file " + filename +" is not a plain text file")
            break
        else: keywordFinder(filename)

    # for key in keywordDict:
    #     if(keywordDict[key] > 1):
    #         print(key + "           " + str(keywordDict[key]))

    #Stage 1.1: create folders
    #add new keywords from all files to dictionary, if already in dictionary, ++
    for key in keywordDict:
        if(keywordDict[key] > 1):
            makeFolder(folderPath, key)
        else: del key

    for filename in os.listdir(path):
        addToFolder(filename)

    for key in keywordDict:
        if(os.listdir(path+key) == ""):
            os.rmdir(path+key)


def addToFolder(filename):
    os.chdir(folderPath)
    with open(filename, 'r', errors="replace") as dirFile:
        fileText = dirFile.read()
        r=Rake()
        r.extract_keywords_from_text(fileText)
        keywords = r.get_ranked_phrases()


    for word in keywords[0:5]:
        for key in keywordDict:
            if(word==key):
                placeInFolder(folderPath, filename)
                break






def keywordFinder(filename):
    os.chdir(folderPath)
    with open(filename, 'r', errors="replace") as dirFile:
        fileText = dirFile.read()
        r=Rake()
        r.extract_keywords_from_text(fileText)
        keywords = r.get_ranked_phrases()

    for word in keywords[0:5]:
        if(word in keywordDict):
            keywordDict[word]+=1
        else:
            keywordDict[word] =1


#model = gensim.models.Word2Vec.load(os.getcwd()+"/AI")
#print(str(model.most_similar(keyword)))


fileOrganizer(folderPath)

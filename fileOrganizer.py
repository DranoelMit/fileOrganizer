import os
import nltk
import gensim
from fold import makeFolder, placeInFolder
from gensim import corpora, models, similarities
from rake_nltk import Rake


folderPath = input("Enter the path you would like to organize: ")
keywordDict ={}
fileTexts= {}
keyLst2Del =[] #keywords that did not have matches in Stage 1
textLst2Del ={} #The files that DID have matches in Stage 1
ogKeywordRels = {}


def fileOrganizer(path):
    #Stage 1.0: find keywords in each file
    for filename in os.listdir(path):
        if(filename[filename.rfind('.'):] != '.txt'):
            print("ERROR: the file " + filename +" is not a plain text file")
            break
        else: keywordFinder(filename)

    # for key ipythn keywordDict:
    #     if(keywordDict[key] > 1):
    #         print(key + "           " + str(keywordDict[key]))

    #Stage 1.1: create folders
    #add new keywords from all files to dictionary, if already in dictionary, ++

    for key in keywordDict:
        if(keywordDict[key] > 1):
            makeFolder(folderPath, key)
        else: keyLst2Del.append(key)

    for word in keyLst2Del:
        del keywordDict[word]

    addToFolder()

    for key in keywordDict:
        if(os.listdir(str(path+"/"+key).replace("\"","")) == ""):
            os.rmdir(path+key)

    for title in textLst2Del:
        del fileTexts[title]
    #Stage 2.0: create lists of related words to each keyword, then try and make matches that way


    for keyword in keyLst2Del:
        findRelKeywords(keyword)

    for key in keywordDict:
        if(keywordDict[key] > 1):
            try:
                makeFolder(folderPath, key)
            except FileExistsError:
                print("file already exists")

    for key in fileTexts:
        for lstRelKeyword in ogKeywordRels:
            for i in ogKeywordRels[lstRelKeyword]:
                if(lstRelKeyword in fileTexts[key] and keywordDict[i] > 1):
                    placeInFolder(folderPath, i, key)




    #NEED TO FIND WHICH FILES HAVE THE KEYWORDS THAT MADE THE RELATION FOLDERS & ADD THEM TO IT
        #Added dict list of keywords and the relkeywords that branched from the





def addToFolder():
    for filename in fileTexts:
        r=Rake()
        r.extract_keywords_from_text(fileTexts[filename])
        keywords = r.get_ranked_phrases()

        for key in keywordDict:
            for word in keywords[0:5]:
                if(word==key):
                    placeInFolder(folderPath, word, filename)
                    textLst2Del[filename] =fileTexts[filename]
                    break



def keywordFinder(filename):
    os.chdir(folderPath)
    dirFile= open(filename, 'r', errors="replace")
    fileTexts[filename]= dirFile.read()
    dirFile.close()
    r=Rake()
    r.extract_keywords_from_text(fileTexts[filename])
    keywords = r.get_ranked_phrases()

    for word in keywords[0:5]:
        if(word in keywordDict):
            keywordDict[word]+=1
        else:
            keywordDict[word] =1

def findRelKeywords(keyword):
    similars = []
    for i in range(5):
        try:
            similars.append(model.most_similar(keyword)[i])
        except KeyError:
                print(keyword + " is not accepted by Word2Vec")
    for item in similars:
            word = str(item)[3:str(item).rfind("\'")]
            if(word in keywordDict):
                keywordDict[word]+=1
            else:
                keywordDict[word]=1
                ogKeywordRels[keyword].append(word)





#has to happen before everything else
model = gensim.models.Word2Vec.load(os.getcwd()+"/AI")


#start the code
fileOrganizer(folderPath)

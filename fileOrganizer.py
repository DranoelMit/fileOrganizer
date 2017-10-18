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
ogKeywordRels = {} # "relWord1,relWord2,....."


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
            keywordDict[key] =0
        else: keyLst2Del.append(key)

    for word in keyLst2Del:
        del keywordDict[word]

    addToFolder()

    for key in keywordDict:
        if(len(os.listdir(str(path+"/"+key).replace("\"","").replace(" ",""))) == 0):
            os.rmdir(str(path+"/"+key).replace("\"","").replace(" ",""))


    for title in textLst2Del:
            del fileTexts[title]

            #AT THIS POINT, the only text files left are the ones not in folders




    #Stage 2.0: create lists of related words to each keyword, then try and make matches that way


    #This is sending list of words without matches
    for keyword in keyLst2Del:
        ogKeywordRels[keyword]=[]
        findRelKeywords(keyword)

    for key in keywordDict:
        if(keywordDict[key] > 1):
                makeFolder(folderPath, key)

    for key in keywordDict:
        if(keywordDict[key] > 1):
            for txtfile in fileTexts:
                for word in keyLst2Del:
                    if(word in fileTexts[txtfile] and key in ogKeywordRels[word]):
                        if(txtfile in os.listdir(folderPath)):
                            placeInFolder(folderPath, key, txtfile)
                        break

    for key in keywordDict:
        if(keywordDict[key] > 1 and len(os.listdir(str(path+"/"+key).replace("\"","").replace(" ",""))) == 0):
            os.rmdir(str(path+"/"+key).replace("\"","").replace(" ",""))

            #NEED TO: check for each rel keyword that has multiple tallis,

            #for each file, check each keyword, if that keyword is in ogKeywordRels

            # then check each word in that value array to see if == word with multiple tallies

            #if so, add to folderPath




def addToFolder():
    for filename in fileTexts:
        r=Rake()
        r.extract_keywords_from_text(fileTexts[filename])
        keywords = r.get_ranked_phrases()

        for key in keywordDict:
            for word in keywords[0:5]:
                if(word==key and filename in os.listdir(str(folderPath).replace("\"","").replace(" ",""))):
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
            word = str(item)[2:str(item).rfind("\'")]

            if(word in keywordDict):
                keywordDict[word]+=1
            else:
                keywordDict[word] =1
                ogKeywordRels[keyword].append(word)

#I now have:
# ogKeywordRels keyword = [relWord1,relWord2, .....]
#keywordDict now has tallies of related words






#has to happen before everything else
model = gensim.models.Word2Vec.load(os.getcwd()+"/AI")


#start the code
fileOrganizer(folderPath)

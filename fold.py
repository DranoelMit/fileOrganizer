import os


def makeFolder(folderPath, folderName):
    os.mkdir(folderPath+"/"+folderName.replace("\"",""))

def placeInFolder(folderPath, fileName):
    os.rename(folderPath,folderPath+"/"+fileName)

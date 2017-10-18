import os


def makeFolder(folderPath, folderName):
    os.mkdir(folderPath+"/"+''.join(e for e in folderName if e.isalnum()))

def placeInFolder(folderPath, subFolder, filename):
        os.rename(folderPath+"/"+filename, folderPath+"/"+''.join(e for e in subFolder if e.isalnum())+"/"+filename)

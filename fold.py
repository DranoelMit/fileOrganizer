import os


def makeFolder(folderPath, folderName):
    os.mkdir(folderPath+"/"+folderName.replace("\"","").replace(" ",""))

def placeInFolder(folderPath, subFolder, filename):
        os.rename(folderPath+"/"+filename,  folderPath+"/"+subFolder.replace("\"","").replace(" ","")+"/"+filename)

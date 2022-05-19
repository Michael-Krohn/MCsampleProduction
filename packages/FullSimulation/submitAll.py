import os
import csv
import time

oldFile = open("currentSteps.csv", "r")
oldData = csv.reader(oldFile)


for submission in oldData:
    datasetName = submission[0]
    os.system("python3 submitNextStep.py "+datasetName)
    time.sleep(2)

oldFile.close()
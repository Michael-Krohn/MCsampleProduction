
import os
import time
import csv

#make sure the input csv is ready before you call this script!
# If the file requires an SLHA file, make sure to have that file in skeleton/SLHA
os.system("python config_GEN.py inputs.csv")
time.sleep(0.1)
with open("inputs.csv", 'r') as f:
    # Retrieves the name of the dataset along with the generator fragment
    inputs = csv.reader(f)
    for Input in inputs:
        datasetName = Input[0]
        genFragment = Input[1]
    with open("skeleton/genfragments/"+genFragment,'r') as fragmentFile:
        fragmentFileLines = fragmentFile.readlines()
        SLHAFile = None
        for i in range(len(fragmentFileLines)): # Checks if there is an SLHA file needed and if so saves its name
            currentLine = fragmentFileLines[i]
            SLHALineIndex = currentLine.find("SLHA:file")
            if SLHALineIndex != -1:
                SLHAFile = currentLine[SLHALineIndex+12:-3]
        if SLHAFile != None:
            with open("inputs/"+datasetName+"/submit_crab.py", 'r') as submitCrab:
                lines = submitCrab.readlines()
                location = os.getcwd()
                inputFilesLine = "config.JobType.inputFiles = [\""+location+"/skeleton/SLHA/"+SLHAFile+"\"]\n"
                lines.insert(lines.index("config.JobType.psetName = \"run_crab.py\"\n")+1, inputFilesLine)
            with open("inputs/"+datasetName+"/submit_crab.py", 'w') as submitCrab:
                submitCrab.writelines(lines)

os.system("chmod +x submit_crab_inputs.sh")
os.system("./submit_crab_inputs.sh")
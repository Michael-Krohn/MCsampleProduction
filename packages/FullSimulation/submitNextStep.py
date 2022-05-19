import os
import subprocess
from argparse import ArgumentParser
import csv
import sys
import shutil

##Add Info on How to Use##
# 1. Run prepare.py with proper inputs to prepare csv data for task
# 2. Run command "python3 submitNextStep.py" with an argument of the name of the dataset for the intended task
# 2b. The following option are also available:
# -p to set a minimum submitted to total jobs ratio in order to move on to next step
# -lastStep to set the intended last step needed for this job

## Add description of function ##
def scrape_dataset_name(crabOutput):
    if("Output dataset:" in crabOutput):
        lines = crabOutput.split('\n')
        for line in lines:
            if("Output dataset:" in line):
                # print("crab task completed, returning dataset name")
                print("dataset found, returning dataset name")
                print(line.split()[2])
                return line.split()[2]
    ## Error: no dataset does not imply that the job was not completed, only that no jobs have been published
    print("Dataset name not found - either the job wasn't completed or the crab status has expired")
    os.system("cd ..")
    raise ValueError("task not finished running or never submitted in the first place, no output dataset name available")

## Add description of function ##
def scrape_completion_percentage(crabOutput):
    if "dataset(s):\tdone" in crabOutput:
        lines = crabOutput.split('\n')
        for line in lines:
            if("dataset(s):\tdone" in line):
                tempIndex = line[line.index("dataset(s):\tdone")+27:line.index("%")]
                return float(tempIndex)/100
    else:
        return 0.0

#Parses input for the intended name of dataset and temporary minimum completion percentage
parser = ArgumentParser()
parser.add_argument("datasetName")
parser.add_argument("-p")
datasetName = parser.parse_args().datasetName
currentP = parser.parse_args().p
print("Dataset Name: " + datasetName + "\n")
# print("Minimum completion percentage: ", int(currentP)*100)

if currentP != None: # Checks if inputted value is valid
    try:
        currentP = float(currentP)
        if currentP < 0 or currentP > 1:
            print("Value for p must be between 0 and 1")
            sys.exit()
    except ValueError:
        print("Invalid Value for p")
        sys.exit()


steps = ["GEN__CMSSW_10_6_22", "SIM__CMSSW_10_6_17_patch1", "DIGIPremix__CMSSW_10_6_17_patch1", "HLT__CMSSW_9_4_14_UL_patch1", "RECO__CMSSW_10_6_17_patch1", "MiniAOD__CMSSW_10_6_17_patch1", "NanoAODv2__CMSSW_10_6_19_patch2","Completion"]

try:
    with open("currentSteps.csv", "r") as f:
        currentSteps = csv.reader(f)
        foundRow = False
        # Checks if there is data saved for the dataset
        for submission in currentSteps:
            # print(submission[0])
            if submission[0] == datasetName:
                # Uses saved p if -p option is not used
                foundRow = True
                if currentP == None:
                    currentP = float(submission[1])
                currentStep = submission[2]
                lastStep = submission[3]
        if not foundRow:
            print("Corresponding row for \'" + datasetName + "\'not found in currentSteps.csv")
            sys.exit()
except FileNotFoundError:
    print("\'currentsSteps.csv\' not found! Prepare proper \'inputs.csv\' file in GEN__CMSSW_10_6_22/src/ and run prepare.py before continuing")
    sys.exit()

# Checks if attempted step already has project folder with dataset name
projectDirectory = currentStep + "/src/inputs/" + datasetName
if os.path.exists(projectDirectory):
    print(projectDirectory + " already exists")
    deleteDirectory = input("Would you like to delete this project directory and continue: y/n? ")
    while deleteDirectory != "y" and deleteDirectory != "n":
        print("Invalid Input!")
        deleteDirectory = input("Would you like to delete this project directory and continue: y/n? ")
    if deleteDirectory == "y":
        os.system("rm -r " + projectDirectory)
    else:
        raise ValueError("Project directory exists and was not deleted, therefore cannot continue to crab submission")
    
if(currentStep == "GEN__CMSSW_10_6_22"):
        setname = ""
else:
    try:
        # Retrieves the output dataset and the percentage of jobs published
        crabOutput = subprocess.getoutput("crab status -d " + steps[steps.index(currentStep)-1] + "/src/inputs/" + datasetName + "/crab_projects/crab_" + datasetName)
        # print(crabOutput)
        setname = scrape_dataset_name(crabOutput)
        completionPercentage = scrape_completion_percentage(crabOutput)
        print("Submission", completionPercentage*100, "percent published")
        ## Fix exit text and logic behind errors! ##
        if completionPercentage < currentP:
            raise ValueError("Completion Status Does not surpass minimum to move on")
    except ValueError:
        print("not done with previous job!")
        sys.exit()

lastStepIndex = steps.index(lastStep)
currentStepIndex = steps.index(currentStep)
if currentStepIndex <= lastStepIndex:
    os.chdir(currentStep + "/src")
    os.system("python3 run_step.py " + datasetName + " " + setname)
    os.chdir("../..")

oldFile = open("currentSteps.csv", "r")
oldData = csv.reader(oldFile)
newData = []
for submission in oldData:
    if submission[0] == datasetName:
        if currentStepIndex != lastStepIndex + 1:
            submission[2] = steps[steps.index(currentStep)+1] # Increments the saved step for the dataset
        else:
            print("Last step completed, no more steps to run")
            continue # Skips dataset
    newData.append(submission)
oldFile.close()

newFile = open("currentSteps.csv", "w")
newFileWriter = csv.writer(newFile)
newFileWriter.writerows(newData)
newFile.close()

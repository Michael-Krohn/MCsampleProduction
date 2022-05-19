import argparse
import csv
import os
import sys

##Add info on how to use##
# 1. Create the file, "inputs.csv" in GEN__CMSSW_10_6_22/src/ in the format of datasetname,genfragment,numEvents,numJobs
# 2. Run "python3 prepare.py "
# 2b. The following options can be used:
# -p to set a minimum submitted jobs to total jobs ratio to move onto the next step
# -lastStep to set an intended last step for this task

# Parses input for a default minimum completion percentage
parser = argparse.ArgumentParser()
parser.add_argument("-p", default=1)
p = parser.parse_args().p
parser.add_argument("-lastStep", default="NanoAOD")
lastStep = parser.parse_args.lastStep

try:
    p = float(p)
    if p < 0 or p > 1:
        print("value for p must be between 0 and 1")
        sys.exit()
except ValueError:
    print("Invalid Value for p")
    sys.exit()
    
lastStepOptions = ["GEN__CMSSW_10_6_22", "SIM__CMSSW_10_6_17_patch1", "DIGIPremix__CMSSW_10_6_17_patch1", "HLT__CMSSW_9_4_14_UL_patch1", "RECO__CMSSW_10_6_17_patch1", "MiniAOD__CMSSW_10_6_17_patch1", "NanoAODv2__CMSSW_10_6_19_patch2","Completion"]
while lastStep not in lastStepOptions:
    lastStep = input("Invalid Last Step Choice!\nLast Step Options are "+str(lastStepOptions) + ": ")
print("Chosen Last Step: " + lastStep)

# Retrieves the intended dataset name
try:
    with open("GEN__CMSSW_10_6_22/src/inputs.csv", "r") as f:
        inputs = csv.reader(f)
        ##Add check correct information in file##
        for entry in inputs:
            datasetName = entry[0]
except FileNotFoundError:
    print("inputs.csv not found in GEN__CMSSW_10_6_22/src")
    sys.exit()


try:
    oldSteps = open("currentSteps.csv","r")
    currentSteps = csv.reader(oldSteps)
    # Checks if the dataset name is already in the saved data
    for submission in currentSteps:
        if submission[0] == datasetName:
            print(datasetName + " already exists in currentSteps.csv")
            sys.exit()
    oldSteps.close()
except IndexError:
    pass
except FileNotFoundError:
    pass


newSteps = open("currentSteps.csv","a")
csv_writer = csv.writer(newSteps)
csv_writer.writerow([datasetName, p, "GEN__CMSSW_10_6_22", lastStep]) # Appends new data to end of file
newSteps.close()

os.system("python3 submitNextStep.py " + datasetName) # Runs GEN on the dataset
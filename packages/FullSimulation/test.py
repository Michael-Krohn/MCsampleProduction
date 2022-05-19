# import os

# if os.path.exists("GEN__CMSSW_10_6_22"):
#     print("yes")
# else:
#     print("no")

# datasetName = "DoublyChargedHiggsToTau"
# currentStep = "GEN__CMSSW_10_6_22"
# if os.path.exists(currentStep + "/src/inputs/" + datasetName + "/crab_projects/crab_" + datasetName):
#     print("yes")
# else:
#     print("no")

# if os.path.exists(currentStep + "/src/inputs/" + datasetName + "/crab_projects/crab_" + datasetName):
#     print(currentStep + "/src/inputs/" + datasetName + "/crab_projects/crab_" + datasetName + " already exists")
#     deleteDirectory = input("Would you like to delete this project directory and continue: y/n? ")
#     while deleteDirectory != "y" and deleteDirectory != "n":
#         print("Invalid Input!")
#         deleteDirectory = input("Would you like to delete this project directory and continue: y/n? ")
#     if deleteDirectory == "y":
#         print("Deleted")
#     else:
#         raise ValueError("Project directory exists and was not deleted, therefore cannot continue to crab submission")

# import argparse

# x = input()
# parser = argparse.ArgumentParser()
# parser.add_argument("-a", default=1)
# currenta = parser.parse_args().a
# parser.add_argument("-b", default=x)
# currentb = parser.parse_args().b
# print(currenta)
# print(currentb)

# lastStep = input("Choose: ")
# lastStepOptions = ["GEN", "SIM", "DIGIPremix", "HLT", "RECO", "MiniAOD", "NanoAOD"]
# if lastStep != "":
#     while lastStep not in lastStepOptions:
#         lastStep = input("Invalid Last Step Choice!\nLast Step Options are "+str(lastStepOptions) + ": ")
# print("Chosen Last Step: " + lastStep)
import os
import csv

suffixes = ["0_9"]

for i in range(len(suffixes)):
    suffix = suffixes[i]
    inputFile = open("GEN__CMSSW_10_6_22/src/inputs.csv", "w")
    datasetName = "LeptonJetMass"+suffix
    fragmentFile = "pythiaFragmentLeptonJetMass"+suffix+".py"
    numEvents = 30000
    numJobs = 60
    csv_writer = csv.writer(inputFile)
    csv_writer.writerow([datasetName, fragmentFile, numEvents, numJobs]) # Appends new data to end of file
    inputFile.close()

    os.system("cp ~/nobackup/CRABNew/CMSSW_11_0_2/src/Datacards/leptonJetWithHadronization/"+fragmentFile + " GEN__CMSSW_10_6_22/src/skeleton/genfragments/")
    os.system("python3 prepare.py -p 0.97")

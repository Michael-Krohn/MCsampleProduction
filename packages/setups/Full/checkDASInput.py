import os

def printDASInputError(inputdataset,oldstep,step,campaign):

    print "[ERROR] INPUTDATASET error due to one of the two following reasons : "
    print "[ERROR] >>     1. Input for "+step+" should be "+oldstep
    print "[ERROR] >>     2. Campaign is not matching (e.g. 2017 input for 2017 production)"

def checkDASInput(inputdataset,step,campaign):

    steps = ["SIM","DIGIPremix","HLT","RECO","MiniAOD","NanoAODv2"]

    for i_step in range(len(steps)):

        if step == steps[i_step]:

            if i_step == 0:
                if "wmLHEGEN" in inputdataset:
                    oldstep = "wmLHEGEN"
                elif "GEN" in inputdataset:
                    oldstep = "GEN"
            else:
                oldstep = steps[i_step-1]

            tag = campaign+"_"+oldstep
            if tag in inputdataset:
                return False
            else:
                printDASInputError(inputdataset,oldstep,step,campaign)
                return True


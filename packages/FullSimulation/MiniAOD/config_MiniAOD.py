import os
import sys
import argparse
sys.path.append("../../../../packages/setups/Full/")
import checkDASInput

def exit_argumenterr():
        print "[EXIT] Input arguments are not correctly given"
        print "[EXIT] <inputfile.dat> should contain : DATASETNAME INPUTDATASET"
        print "[EXIT] DATASETNAME : Name of the dataset that will be used for DAS publication"
        print "[EXIT] INPUTDATASET : DAS published dataset"
        print "[EXIT] e.g.) TTbarTypeIHeavyN-Mu_4L_LO_MN60 /TTbarTypeIHeavyN-Mu_4L_LO_MN60/jihunk-DRPremix_step1__CMSSW_10_2_5-96e2d90999375d8c542ea905b43803e1/USER"
        sys.exit()

def print_sampleinfo(datasetname,inputdataset,inputname):
        print "[INFO] Reading list of samples to be submitted : "+inputname
        print "[INFO] Generating configuration files for "+datasetname
        print "[INFO]      Using "+inputdataset
        check_argument(datasetname,inputname)

def check_argument(datasetname,inputname):
        if os.path.isdir(inputname+"/"+datasetname):
          print "[EXIT] Directory "+inputname+"/"+datasetname+" already exists"
          sys.exit()

parser = argparse.ArgumentParser()
parser.add_argument("input_f")
parser.add_argument("--dev", action = "store_true")
input_f = parser.parse_args().input_f
inputname = input_f.split(".")[0]
dev = parser.parse_args().dev

cwd = os.getcwd()
datasettag = cwd.split("/")[-2]
step =datasettag.split("__")[0]
campaign = cwd.split("/")[-3]

list_f = open(input_f,"r")
list_ls = list_f.readlines()
list_f.close()

cmsdriver_campaign_f = open("skeleton/cmsdriver_"+step+".dat","r")
cmsdriver_campaign_ls = cmsdriver_campaign_f.readlines()
for cmsdriver_campaign_l in cmsdriver_campaign_ls:
  cmsdriver_campaign_l = cmsdriver_campaign_l.strip().split("\t")
  if campaign == cmsdriver_campaign_l[0]:
    add_cmsdriver = cmsdriver_campaign_l[1]

cmsdriver_campaign_f.close()

submit_list = []

run_cmsdriver_sh = open("run_cmsdriver_"+inputname+".sh","w")
run_cmsdriver_sh.write("#!/bin/bash\n")
run_cmsdriver_sh.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
run_cmsdriver_sh.write("cmsenv\n")
run_cmsdriver_sh.write("scram b -j 4\n")

submit_crab_sh = open("submit_crab_"+inputname+".sh","w")
submit_crab_sh.write("#!/bin/bash\n")
submit_crab_sh.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
submit_crab_sh.write("cmsenv\n")

for list_l in list_ls:
  list_l = list_l.strip().replace(" ",",").replace("\t",",").split(",")
  if len(list_l) != 2:
    exit_argumenterr()
  datasetname = list_l[0]
  inputdataset = list_l[1]
  if checkDASInput.checkDASInput(inputdataset,step,campaign):
    sys.exit()
  print_sampleinfo(datasetname,inputdataset,inputname)

  submit_list.append(datasetname)
  crabwd = inputname+"/"+datasetname+"/"
  os.system("mkdir -p "+crabwd)

  os.system("cp skeleton/submit_crab.py "+crabwd+"/submit_crab.py")
  os.system("sed -i 's|###REQUESTNAME###|"+datasetname+"|g' "+crabwd+"/submit_crab.py")
  os.system("sed -i 's|###INPUTDATASET###|"+inputdataset+"|g' "+crabwd+"/submit_crab.py")
  os.system("sed -i 's|###INPUTDATASETTAG###|"+campaign+"_"+step+"|g' "+crabwd+"/submit_crab.py")
#  os.system("sed -i 's|###UNITSPERJOB###|"+str(int(nevents)/int(nsplitjobs))+"|g' "+datasetname+"/submit_crab.py")

  cmsdriver_sh = open(crabwd+"/run_cmsdriver.sh","w")
  cmsdriver_l = "cmsDriver.py step1 --no_exec --mc --python_filename run_crab.py --fileout "+step+".root --eventcontent MINIAODSIM --runUnscheduled --datatier MINIAODSIM --geometry DB:Extended --step PAT -n 6284 "+add_cmsdriver 
  cmsdriver_sh.write("#!/bin/bash\n")
  cmsdriver_sh.write(cmsdriver_l+"\n")
  cmsdriver_sh.close()

  run_cmsdriver_sh.write("cd "+cwd+"/"+crabwd+"/\n")
  run_cmsdriver_sh.write("chmod a+x ./run_cmsdriver.sh\n")
  run_cmsdriver_sh.write("source ./run_cmsdriver.sh\n")

  submit_crab_sh.write("cd "+cwd+"/"+crabwd+"/\n")
  submit_crab_sh.write("crab submit -c submit_crab.py\n")

run_cmsdriver_sh.write("cd "+cwd+"/\n")
run_cmsdriver_sh.close()

submit_crab_sh.write("cd "+cwd+"/\n")
submit_crab_sh.close()

os.system("source ./run_cmsdriver_"+inputname+".sh")
os.system("rm ./run_cmsdriver_"+inputname+".sh")

print "[INFO] cmsDriver build for datasets below have completed"
for i_submit in range(len(submit_list)):
  print "[INFO] >>      "+submit_list[i_submit]
print "[INFO] Execute the command to submit the jobs to CRAB"
print "[INFO] >>     voms-proxy-init"
print "[INFO] >>     source submit_crab_"+inputname+".sh"

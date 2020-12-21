import os
import sys
import random
import argparse

def exit_argumenterr():
	print "[EXIT] Input arguments are not correctly given"
	print "[EXIT] <inputfile.dat> should contain : DATASETNAME OUTPUTDATASET"
	print "[EXIT] DATASETNAME : Name of the dataset that will be used for DAS publication"
        print "[EXIT] OUTPUTDATASET : DAS published dataset"
        print "[EXIT] e.g.) TTbarTypeIHeavyN-Mu_4L_LO_MN60 /TTbarTypeIHeavyN-Mu_4L_LO_MN60/jihunk-DRPremix_step1__CMSSW_10_2_5-96e2d90999375d8c542ea905b43803e1/USER"
	sys.exit()

def print_sampleinfo(datasetname,outputdataset):
        print "[INFO] Generating configuration files for "+datasetname
        print "[INFO]      Using "+outputdataset
        check_arguement(datasetname)

def check_argument(datasetname):
	if not os.path.isdir(datasetname):
	  print "[EXIT] Directory "+datasetname+" already exists"
	  sys.exit()

parser = argparse.ArgumentParser()
parser.add_argument("input_f")
parser.add_argument("--dev", action = "store_true")
input_f = parser.parse_args().input_f
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

os.system("mkdir -p Configuration/GenProduction/python/")
submit_list = []

for list_l in list_ls:
  list_l = list_l.strip().replace(" ",",").replace("\t",",").split(",")
  if len(list_l) != 2:
    exit_argumenterr()
  datasetname = list_l[0]
  outputdataset = list_l[1]

  print_sampleinfo(datasetname,outputdataset)

  submit_list.append(datasetname)
  os.system("mkdir -p "+datasetname)

  os.system("cp skeleton/submit_crab.py "+datasetname+"/")
  os.system("sed -i 's|###REQUESTNAME###|"+datasetname+"|g' "+datasetname+"/submit_crab.py")
  os.system("sed -i 's|###OUTPUTPRIMARYDATASET###|"+datasetname+"|g' "+datasetname+"/submit_crab.py")
  os.system("sed -i 's|###OUTPUTDATASETTAG###|"+campaign+"_"+step+"|g' "+datasetname+"/submit_crab.py")
  os.system("sed -i 's|###UNITSPERJOB###|"+str(int(nevents)/int(nsplitjobs))+"|g' "+datasetname+"/submit_crab.py")
  os.system("sed -i 's|###NJOBS###|NJOBS="+nsplitjobs+"|g' "+datasetname+"/submit_crab.py")

  os.system("mkdir -p "+datasetname)
  cmsdriver_sh = open(datasetname+"/run_cmsdriver.sh","w")
  cmsdriver_l = "cmsDriver.py step1 --no_exec --mc --python_filename run_crab.py --fileout "+step+".root --eventcontent RAWSIM --datatier GEN-SIM --runUnscheduled --step SIM --geometry DB:extended -n 6284 "+add_cmsdriver 
  cmsdriver_sh.write("#!/bin/bash\n")
  cmsdriver_sh.write(cmsdriver_l+"\n")
  cmsdriver_sh.close()

run_cmsdriver_sh = open("run_cmsdriver_"+input_f.split(".")[0]+".sh","w")
run_cmsdriver_sh.write("#!/bin/bash\n")
run_cmsdriver_sh.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
run_cmsdriver_sh.write("cmsenv\n")
for i_submit in range(len(submit_list)):
  run_cmsdriver_sh.write("cd "+cwd+"/"+datasetname+"/\n")
  run_cmsdriver_sh.write("crab submit -c submit_crab.py\n")
run_cmsdriver_sh.write("cd "+cwd+"/"+datasetname+"/\n")
run_cmsdriver_sh.close()

os.system("source run_cmsdriver_"+input_f.split(".")[0]+".sh")
print "[INFO] cmsDriver build for datasets below have completed"
for i_submit in range(len(submit_list)):
  print "[INFO]      "+submit_list[i_submit]
print "[INFO] Execute the command to submit the jobs to CRAB"
print "[INFO]      source submit_crab_"+input_f.split(".")[0]+".sh"

import os
import sys
import random
import argparse

def exit_argumenterr():
	print "[EXIT] Input arguments are not correctly given"
	print "[EXIT] <inputfile.dat> should contain : DATASETNAME GENFRAGMENT NEVENTS NSPLITJOBS GRIDPACK"
	print "[EXIT] DATASETNAME : Name of the dataset that will be used for DAS publication"
	print "[EXIT] GENFRAGMENT : Generator fragment python files that will be used for hadronizer or generator"
	print "[EXIT]               Should be stored in skeleton/genfragments directory"
	print "[EXIT] NEVENTS : Number of events in total that will be made"
	print "[EXIT]           Jet matching or filter efficiencies should be taken into account"
	print "[EXIT]           e.g.) efficiency is 40% => NEVENTS=10000 will give 4000 event after GEN step"
        print "[EXIT] NSPLITJOBS : Number of jobs that will be splitted into CRAB"
	print "[EXIT]              NEVENTS=10000 and NSPLITJOBS=4 => 2500 events per CRAB job"
        print "[EXIT] GRIDPACK : Path to gridpack"
        print "[EXIT] e.g.) DYtoMuMu Hadronizer_TuneCP5_13TeV_generic_LHE_pythia8_PSweights_cff.py 10000 4 /PATH/TO/GRIDPACK"
	sys.exit()

def print_sampleinfo(datasetname,genfragment,nevents,nsplitjobs,gridpack):
        print "[INFO] Generating configuration files for "+datasetname
        print "[INFO]      "+nevents+" events splitted into "+nsplitjobs+" jobs"
        print "[INFO]      Using "+gridpack
        print "[INFO]      Using "+genfragment
        check_arguement(datasetname,genfragment,nevents,nsplitjobs,gridpack)

def check_argument(datasetname,genfragment,nevents,nsplitjobs,gridpack):
	if not os.path.isdir(datasetname):
	  print "[EXIT] Directory "+datasetname+" already exists"
	  sys.exit()
	if not os.path.exists("skeleton/genfragments/"+genfragment):
	  print "[EXIT] "+genfragment+" not found in skeleton/genfragments/"
	  sys.exit()
	if not (int(nevents)/int(nsplitjobs) == float(nevents)/int(nsplitjobs)):
	  print "[EXIT] NEVENTS/NSPLITJOBS is not an integer"
	  sys.exit()
	if "cvmfs" in gridpack:
	  if not os.path.exists(gridpack):
	    print "[EXIT] "+gridpack+" not found"
	    sys.exit()
	elif "eos" in gridpack:
	  if "lxplus" in os.getenv("HOSTNAME"):
	    if not os.path.exists(gridpack):
	      print "[EXIT] "+gridpack+" not found"
	      sys.exit()
	  else:
	    print "[WARN] "+gridpack+" should be in lxplus.cern.ch"
	else:
	  print "[EXIT] GRIDPACK should be in either CVMFS or EOS area in lxplus"
	  sys.exit()

parser = argparse.ArgumentParser()
parser.add_argument("input_f")
parser.add_argument("--nowmLHE", action = "store_true")
parser.add_argument("--dev", action = "store_true")
input_f = parser.parse_args().input_f
nowmLHE = parser.parse_args().nowmLHE
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
  if len(list_l) != 5:
    exit_argumenterr()
  datasetname = list_l[0]
  genfragment = list_l[1].replace("skeleton/","").replace("genfragments/","")
  nevents = list_l[2]
  nsplitjobs = list_l[3]
  gridpack = list_l[4]

  print_sampleinfo(datasetname,genfragment,nevents,nsplitjobs,gridpack)

  submit_list.append(datasetname)
  os.system("mkdir -p "+datasetname)

  os.system("cp skeleton/genfragments/"+genfragment+" Configuration/GenProduction/python/"+datasetname+".py")
  os.system("sed -i 's|###GRIDPACK###|"+gridpack+"|g' Configuration/GenProduction/python/"+datasetname+".py")

  os.system("cp skeleton/submit_crab.py "+datasetname+"/")
  os.system("sed -i 's|###REQUESTNAME###|"+datasetname+"|g' "+datasetname+"/submit_crab.py")
  os.system("sed -i 's|###OUTPUTPRIMARYDATASET###|"+datasetname+"|g' "+datasetname+"/submit_crab.py")
  os.system("sed -i 's|###OUTPUTDATASETTAG###|"+campaign+"_"+step+"|g' "+datasetname+"/submit_crab.py")
  os.system("sed -i 's|###UNITSPERJOB###|"+str(int(nevents)/int(nsplitjobs))+"|g' "+datasetname+"/submit_crab.py")
  os.system("sed -i 's|###NJOBS###|NJOBS="+nsplitjobs+"|g' "+datasetname+"/submit_crab.py")

  os.system("mkdir -p "+datasetname)
  cmsdriver_sh = open(datasetname+"/run_cmsdriver.sh","w")
  cmsdriver_l = "cmsDriver.py Configuration/GenProduction/python/"+datasetname+".py --no_exec --mc --python_filename run_crab.py --fileout "+step+".root  --eventcontent LHE,RAWSIM --datatier LHE,GEN --step LHE,GEN --geometry DB:Extended -n 6284 --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed="+str(random.randint(1, 100000))+" "+add_cmsdriver
  cmsdriver_sh.write("#!/bin/bash\n")
  cmsdriver_sh.write(cmsdriver_l+"\n")
  cmsdriver_sh.close()

run_cmsdriver_sh = open("run_cmsdriver_"+input_f.split(".")[0]+".sh","w")
run_cmsdriver_sh.write("#!/bin/bash\n")
run_cmsdriver_sh.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
run_cmsdriver_sh.write("cmsenv\n")
run_cmsdriver_sh.write("scram b -j 2\n")
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

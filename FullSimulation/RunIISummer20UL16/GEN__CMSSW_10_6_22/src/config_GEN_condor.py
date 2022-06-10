import os
import sys
import random
import argparse

def exit_argumenterr():
        print "[EXIT] Input arguments are not correctly given"
        print "[EXIT] <inputfile.dat> should contain : DATASETNAME GENFRAGMENT NEVENTS NSPLITJOBS"
        print "[EXIT] DATASETNAME : Name of the dataset that will be used for DAS publication"
        print "[EXIT] GENFRAGMENT : Generator fragment python files that will be used for hadronizer or generator"
        print "[EXIT]               Should be stored in skeleton/genfragments directory"
        print "[EXIT] NEVENTS : Number of events in total that will be made"
        print "[EXIT]           Jet matching or filter efficiencies should be taken into account"
        print "[EXIT]           e.g.) efficiency is 40% => NEVENTS=10000 will give 4000 event after GEN step"
        print "[EXIT] NSPLITJOBS : Number of jobs that will be splitted into CRAB"
        print "[EXIT]              NEVENTS=10000 and NSPLITJOBS=4 => 2500 events per CRAB job"
        print "[OPTIONAL] INPUTLHE : Path to LHE file created externally from gridpacks that will be used as an input"
        print "[OPTIONAL]            To use this functionality, --inputLHE should be turned on"
        print "[OPTIONAL]            e.g.) root://cluster142.knu.ac.kr//store/user/shjeon/LHEfiles/DMSimp_monojet_NLO_Axial_GQ0p25_GDM1p0_MY1-1000p0_MXd-1p0.lhe"
        sys.exit()

def print_sampleinfo(datasetname,genfragment,nevents,nsplitjobs,inputname,lhefile):
        print "[INFO] Reading list of samples to be submitted : "+inputname
        print "[INFO] Generating configuration files for "+datasetname
        print "[INFO] >>     "+nevents+" events splitted into "+nsplitjobs+" jobs"
        if (int(nevents)/int(nsplitjobs)) > 2500:
          print "[WARNING] >>     Number of events per CRAB job "+str(int(nevents)/int(nsplitjobs))+" larger than 2500"  
        print "[INFO] >>     Using "+genfragment
        if not lhefile == "":
          print "[INFO] >>     Using "+lhefile
        check_argument(datasetname,genfragment,nevents,nsplitjobs,inputname)

def check_argument(datasetname,genfragment,nevents,nsplitjobs,inputname):
        if os.path.isdir(inputname+"/"+datasetname):
          print "[EXIT] Directory "+inputname+"/"+datasetname+" already exists"
          sys.exit()
        if not os.path.exists("skeleton/genfragments/"+genfragment):
          print "[EXIT] "+genfragment+" not found in skeleton/genfragments/"
          sys.exit()
        if not (int(nevents)/int(nsplitjobs) == float(nevents)/int(nsplitjobs)):
          print "[EXIT] NEVENTS/NSPLITJOBS is not an integer"
          sys.exit()

parser = argparse.ArgumentParser()
parser.add_argument("input_f")
parser.add_argument("--dev", action = "store_true")
parser.add_argument("--inputLHE", action = "store_true")
input_f = parser.parse_args().input_f
inputname = input_f.split(".")[0]
dev = parser.parse_args().dev
inputLHE = parser.parse_args().inputLHE

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

run_cmsdriver_sh = open("run_cmsdriver_"+inputname+".sh","w")
run_cmsdriver_sh.write("#!/bin/bash\n")
run_cmsdriver_sh.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
#run_cmsdriver_sh.write("cmsrel CMSSW_10_6_22\n")
#run_cmsdriver_sh.write("cd CMSSW_10_6_22/src\n")
#run_cmsdriver_sh.write("cmsenv\n")
#run_cmsdriver_sh.write("scram b -j 4\n")

submit_condor_sh = open("submit_condor_"+inputname+".sh","w")

for list_l in list_ls:
  list_l = list_l.strip().replace(" ",",").replace("\t",",").split(",")
  lhefile = ""
  if inputLHE:
    if len(list_l) != 5:
      exit_argumenterr()
    lhefile = list_l[4]
  else:
    if len(list_l) != 4:
      exit_argumenterr()
  datasetname = list_l[0]
  genfragment = list_l[1].replace("skeleton/","").replace("genfragments/","")
  nevents = list_l[2]
  nsplitjobs = list_l[3]

  print_sampleinfo(datasetname,genfragment,nevents,nsplitjobs,inputname,lhefile)

  submit_list.append(datasetname)
  condorwd = inputname+"/"+datasetname+"/"
  os.system("mkdir -p "+condorwd)

  os.system("cp skeleton/genfragments/"+genfragment+" Configuration/GenProduction/python/"+datasetname+".py")

  os.system("cp skeleton/condor_filelist_nEvents.perl "+condorwd+"/condor_filelist_nEvents.perl")

  cmsdriver_sh = open(condorwd+"/run_cmsdriver.sh","w")
  cmsdriver_l = "cmsDriver.py Configuration/GenProduction/python/"+datasetname+".py --no_exec --mc --python_filename run_condor.py --fileout "+step+".root --eventcontent RAWSIM --datatier GEN --step GEN --geometry DB:Extended -n "+str(int(nevents)/int(nsplitjobs))+" "+add_cmsdriver
  if inputLHE:
    cmsdriver_l = cmsdriver_l+" --filein file:"+lhefile
  cmsdriver_sh.write("#!/bin/bash\n")
  cmsdriver_sh.write(cmsdriver_l+"\n")
  cmsdriver_sh.close()

  run_cmsdriver_sh.write("cd "+cwd+"/"+condorwd+"/\n")
  run_cmsdriver_sh.write("chmod a+x ./run_cmsdriver.sh\n")
  run_cmsdriver_sh.write("source ./run_cmsdriver.sh\n")

  os.system("ls "+lhefile+" > LHEfileLocation.txt")
  os.system("sed -i 's;/hdfs;file:/hdfs;' LHEfileLocation.txt")
  os.system("mv LHEfileLocation.txt "+condorwd)

  submit_condor_sh.write("cd "+cwd+"/"+condorwd+"/\n")
  submit_condor_sh.write("./condor_filelist_nEvents.perl run_condor.py LHEfileLocation.txt --jobname "+datasetname+" --nEventsBatch "+str(int(nevents)/int(nsplitjobs))+" --totalEvents "+nevents+"\n")

run_cmsdriver_sh.write("cd "+cwd+"/\n")
run_cmsdriver_sh.close()

submit_condor_sh.write("cd "+cwd+"/\n")
submit_condor_sh.close()

os.system("source ./run_cmsdriver_"+inputname+".sh")
os.system("rm ./run_cmsdriver_"+inputname+".sh")

print "[INFO] cmsDriver build for datasets below have completed"
for i_submit in range(len(submit_list)):
  print "[INFO] >>     "+submit_list[i_submit]
print "[INFO] FOLLOW THESE INSTRUCTIONS TO SUBMIT JOBS TO CONDOR"
print "[INFO] Execute the following commands:"
print "[INFO] >>     cmsenv"
print "[INFO] >>     scram b"
print "[INFO] Open "+cwd+"/"+condorwd+"/run_cmsdriver.sh"
print "[INFO] Copy the command within at run it"
print "[INFO] >>     mv run_condor.py "+condorwd
print "[INFO] >>     source submit_condor_"+inputname+".sh"

#############################################################
# Fast and Full simulation sample production
# Author : Sihyun Jeon (shjeon@cern.ch)
#############################################################

import os
import sys

cwd = os.getcwd()

cmssws = ["slc7_amd64_gcc700", "slc7_amd64_gcc700", "slc7_amd64_gcc700", "slc7_amd64_gcc700"]
cmssws_HLT = ["slc7_amd64_gcc530", "slc7_amd64_gcc530", "slc7_amd64_gcc630", "slc7_amd64_gcc700"]
#methods = ["Full"]#, "Fast"]
methods = ["Fast"]

print "Setting up Fast and Full simulation sample production workflows."
config_storagesite = raw_input("What is your T2/T3 storage site [T2_CH_CERN,T3_KR_KNU,T2_US_FNAL,..]? ")

setup_sh = open("setup.sh", "w")
setup_sh.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")

print "Fetching CMSSW releases for Ultra Legacy sample production."
for i_method in range(0,len(methods)):
  method = methods[i_method]
  if method == "Full":
    campaigns = ["RunIISummer20UL16", "RunIISummer20UL16APV", "RunIISummer20UL17", "RunIISummer20UL18"]
  if method == "Fast":
    campaigns = ["RunIISpring21UL16", "RunIISpring21UL17", "RunIISpring21UL18"]

  for i_campaign in range(0,len(campaigns)):
    campaign = campaigns[i_campaign]
#    print "Fetching CMSSW releases for Ultra Legacy "+method+" "+campaign+"..."
    setup_f = open(cwd+"/packages/setups/"+method+"/setup_"+campaign+".dat")
    setup_ls = setup_f.readlines()
    setup_f.close()

    for i_setup in range(0,len(setup_ls)):
      setup_l =  setup_ls[i_setup].strip()
#      print "\t"+setup_l
      step = setup_l.split("\t")[0]
      cmssw = setup_l.split("\t")[1]
      setup_sh.write("mkdir -p "+cwd+"/"+method+"Simulation/"+campaign+"/\n")
      setup_sh.write("cd "+cwd+"/"+method+"Simulation/"+campaign+"/\n")
      if "HLT" in step:
        setup_sh.write("SCRAM_ARCH='"+cmssws_HLT[i_campaign]+"'\n")
      else:
        setup_sh.write("SCRAM_ARCH='"+cmssws[i_campaign]+"'\n")
      setup_sh.write("scram project -n "+step+"__CMSSW_"+cmssw+" CMSSW CMSSW_"+cmssw+"\n")
      setup_sh.write("cd "+step+"__CMSSW_"+cmssw+"/src/\n")
      setup_sh.write("cp -r "+cwd+"/packages/"+method+"Simulation/"+step+"/* .\n")

setup_sh.write("cd "+cwd+"\n")
setup_sh.write("sed -i 's|###CONFIG_STORAGESITE###|{}|g' ./*Simulation/*/*/src/skeleton/submit_crab.py".format(config_storagesite))
setup_sh.close()
os.system("chmod 755 setup.sh")
os.system("source ./setup.sh")
print "Fetching complete."
print "Steps : (wmLHE)GEN >> SIM >> DIGIPremix >> HLT >> RECO >> MiniAOD >> NanoAODv2"
print "For more details check out :"
print "    EXO-MC&I : https://exo-mc-and-i.gitbook.io/exo-mc-and-interpretation/"
print "    PdmV : https://cms-pdmv.gitbook.io/project/"
print "Make sure you have the writing permissions by executing the command :"
print "    source /cvmfs/cms.cern.ch/crab3/crab.sh"
print "    source /cvmfs/cms.cern.ch/cmsset_default.sh"
print "    cmsrel CMSSW_X_Y_Z"
print "    cd CMSSW_X_Y_Z/src/"
print "    cmsenv"
print "    crab checkwrite --site={}".format(config_storagesite)
os.system("rm setup.sh")

import os
import sys

cwd = os.getcwd()

campaigns = ["RunIISummer20UL16", "RunIISummer20UL16APV", "RunIISummer20UL17", "RunIISummer20UL18"]
cmssws = ["slc7_amd64_gcc700", "slc7_amd64_gcc700", "slc7_amd64_gcc700", "slc7_amd64_gcc700"]
cmssws_HLT = ["slc7_amd64_gcc530", "slc7_amd64_gcc530", "slc7_amd64_gcc630", "slc7_amd64_gcc700"]
methods = ["Full"]#, "Fast"]

print "#############################################################################"
print "#############################################################################"
print ""
print "       Setting up Fast and Full simulation sample production workflows       "
print "       author : Sihyun Jeon (shjeon@cern.ch)                                 "
print ""
print "#############################################################################"
print "#############################################################################"

setup_sh = open("setup.sh", "w")
setup_sh.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")

for i_method in range(0,len(methods)):
  method = methods[i_method]

  for i_campaign in range(0,len(campaigns)):
    campaign = campaigns[i_campaign]
    print "Fetching CMSSW release versions for Ultra Legacy "+method+" "+campaign+"..."
    setup_f = open(cwd+"/packages/setups/"+method+"/setup_"+campaign+".dat")
    setup_ls = setup_f.readlines()
    setup_f.close()

    for i_setup in range(0,len(setup_ls)):
      setup_l =  setup_ls[i_setup].strip()
      print "\t"+setup_l
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
setup_sh.close()	
os.system("chmod 755 setup.sh")
os.system("source ./setup.sh")
os.system("rm setup.sh")

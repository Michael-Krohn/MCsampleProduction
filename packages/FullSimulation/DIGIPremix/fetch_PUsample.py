import os
import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument("campaign")
parser.add_argument("--minimisePU", action = "store_true")
campaign = parser.parse_args().campaign
miniPU = parser.parse_args().minimisePU

pileupinput = ""

if miniPU == True:
  print "[WARNING] Fetching minimal number of Pileup sample files for premixing to boost up the speed for building configuration files"
  print "[WARNING] Sample production requiring large number of events (> 100,000) should not be using this functionality"
  if "16" in campaign:
    NeventsperPUfile = 1600
    NPUfile = 155723
  if "17" in campaign:
    NeventsperPUfile = 9000
    NPUfile = 27105
  if "18" in campaign:
    NeventsperPUfile = 5000
    NPUfile=49576
#  print "[WARNING] 40,000,000 Pileup events will be used for premixing : Fetching "+str(40000000/NeventsperPUfile)+" Pileup sample files"

  pileupinput_f = open("skeleton/PileupInput_"+campaign+".dat")
  pileupinput_ls = pileupinput_f.readlines()
  pileupinput_f.close()

  for i_pileup in range(0,int(5)):#40000000/NeventsperPUfile)):
    pileupinput_l = pileupinput_ls[random.randint(0,NPUfile)].strip()
    pileupinput = pileupinput+"\""+pileupinput_l+"\",\n"

else:
  print "[WARNING] Fetching all the Pileup sample files from DBS, it might take some time to build configuration files"
  print "[WARNING] Sample production not requiring large number of events (< 100,000) is okay to use <--minimisePU> functionality"
  if "16" in campaign:
    pileup_input = "dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL16_106X_mcRun2_asymptotic_v13-v1/PREMIX"
  elif "17" in campaign:
    pileup_input = "dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL17_106X_mc2017_realistic_v6-v3/PREMIX"
  elif "18" in campaign:
    pileup_input = "dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL18_106X_upgrade2018_realistic_v11_L1v1-v2/PREMIX"
    print "[WARNING] >>     "+pileup_input
return pileupinput

import os
import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument("campaign")
parser.add_argument("--minimisePU", action = "store_true")
campaign = parser.parse_args().campaign
miniPU = parser.parse_args().minimisePU

pileup_input = ""

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

  pileup_input_f = open("skeleton/PileupInput_"+campaign+".dat")
  pileup_input_ls = pileup_input_f.readlines()
  pileup_input_f.close()

  print "[INFO] 40,000,000 Pileup events will be used for premixing : Fetching "+str(40000000/NeventsperPUfile)+" Pileup sample files"
  print "[INFO] >>     thisPileupInput_"+campaign+".dat"

  this_pileup_input_f = open("skeleton/thisPileupInput_"+campaign+".dat","a")
  for i_pileup in range(0,int(40000000/NeventsperPUfile)):
    pileup_input_l = pileup_input_ls[random.randint(0,NPUfile)].strip()
    pileup_input = pileup_input+"\""+pileup_input_l+"\","
  this_pileup_input_f.write(pileup_input)
  this_pileup_input_f.close()

#  pileup_input = "###PILEUPINPUT###"

else:
  print "[INFO] Fetching all the Pileup sample files from DBS, it might take some time to build configuration files"
  print "[INFO] Sample production not requiring large number of events (< 100,000) is okay to use <--minimisePU> functionality"
  if "16" in campaign:
    pileup_input = "dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL16_106X_mcRun2_asymptotic_v13-v1/PREMIX"
  elif "17" in campaign:
    pileup_input = "dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL17_106X_mc2017_realistic_v6-v3/PREMIX"
  elif "18" in campaign:
    pileup_input = "dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL18_106X_upgrade2018_realistic_v11_L1v1-v2/PREMIX"
    print "[INFO] >>     "+pileup_input


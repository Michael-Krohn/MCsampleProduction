import os

ff = open("PileupInput_RunIISummer20UL18.dat").readlines()

print len(ff)
print ff[24033]

i=0
for ll in ff:
  i = i+1
print i

import os
import time
import datetime
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("datasetName")
parser.add_argument("outputDataset")
datasetName = parser.parse_args().datasetName
outputDataset = parser.parse_args().outputDataset


with open("inputs.csv", 'w') as f:
    f.write(datasetName+","+outputDataset)

os.system("python config_SIM.py inputs.csv")
time.sleep(0.1)
os.system("chmod +x submit_crab_inputs.sh")
os.system("./submit_crab_inputs.sh")
time.sleep(0.1)
os.remove("inputs.csv")
# os.remove("submit_crab_inputs.sh")
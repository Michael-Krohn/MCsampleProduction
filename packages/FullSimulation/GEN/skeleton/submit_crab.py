from CRABClient.UserUtilities import config, getUsernameFromCRIC

config = config()

config.General.requestName = "###REQUESTNAME###"
config.General.workArea = "crab_projects"
config.General.transferLogs = True
config.General.transferOutputs = True

config.JobType.pluginName = "PrivateMC"
config.JobType.psetName = "run_crab.py"
#config.JobType.maxMemoryMB = 4000
#config.JobType.numCores = 8

config.Data.outputPrimaryDataset = "###OUTPUTPRIMARYDATASET###"
config.Data.outLFNDirBase = "/store/user/%s/" % (getUsernameFromCRIC())#FIXME
config.Data.outputDatasetTag = "###OUTPUTDATASETTAG###"
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = ###UNITSPERJOB###
NJOBS = ###NJOBS###
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = True

config.Site.storageSite = "T3_KR_KNU"

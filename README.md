# MC Sample Production

Setup the code:

```
1. git clone https://github.com/Michael-Krohn/MCsampleProduction.git
2. cd MCsampleProduction/
3. python setup.py
4. cd FullSimulation/RunIISummer20UL16/GEN__CMSSW_10_6_22/src/
```

Create a CSV file with the following info:

1. DATASETNAME : Name of the dataset.
2. GENFRAGMENT : Generator fragment python file that will be used for hadronizer or generator. This should be Hadronizer_TuneCP5_13TeV_MLM_5f_max4j_qCut19_LHE_pythia8_cff.py
3. NEVENTS : Number of events in total that will be made. Jet matching or filter efficiencies should be taken into account. e.g. If matching efficiency is 0.4, and you want 10000 events to be produced, write 10000 X 1/0.4 = 25000.
4. NSPLITJOBS : Number of jobs that will be split into for condor. e.g. NEVENTS=25000 with NSPLITJOBS=25 will run 1000 events per 1 condor job.
5. GRIDPACK : Path to gridpack if gridpack is used. It should be in hdfs area.

An example csv file can be found here: FullSimulation/RunIISummer20UL16/GEN__CMSSW_10_6_22/src/DYJets_m200_GEN.csv

Then run:

```
python config_GEN_condor.py DYJets_m200_GEN_test.csv --inputLHE
```

The script will print out more instructions. Follow these.

### Additional details

For more details check out :

    EXO-MC&I : https://exo-mc-and-i.gitbook.io/exo-mc-and-interpretation/
    PdmV : https://cms-pdmv.gitbook.io/project/

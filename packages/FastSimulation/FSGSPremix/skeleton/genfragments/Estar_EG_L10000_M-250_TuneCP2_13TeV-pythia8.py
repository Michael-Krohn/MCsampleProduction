import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP2Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
        crossSection = cms.untracked.double(1),
        maxEventsToPrint = cms.untracked.int32(0),
        pythiaPylistVerbosity = cms.untracked.int32(1),
        filterEfficiency = cms.untracked.double(1.0),
        pythiaHepMCVerbosity = cms.untracked.bool(False),
        comEnergy = cms.double(13000.),
        PythiaParameters = cms.PSet(
                pythia8CommonSettingsBlock,
                pythia8CP2SettingsBlock,
                pythia8PSweightsSettingsBlock,
                processParameters = cms.vstring( 
                        'ExcitedFermion:qqbar2eStare = on',
                        'ExcitedFermion:Lambda= 10000',
                        '4000011:onMode = off',
                        '4000011:onIfMatch = 11 22',
                        '4000011:m0 = 250'),
                parameterSets = cms.vstring('pythia8CommonSettings',
                                            'pythia8CP2Settings',
                                            'pythia8PSweightsSettings',
                                            'processParameters',
                                            )
                )
) 


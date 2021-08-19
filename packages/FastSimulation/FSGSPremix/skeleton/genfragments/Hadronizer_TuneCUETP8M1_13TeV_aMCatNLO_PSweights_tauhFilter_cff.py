import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *
from Configuration.Generator.Pythia8aMCatNLOSettings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *


generator = cms.EDFilter("Pythia8HadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CUEP8M1SettingsBlock,
        pythia8aMCatNLOSettingsBlock,
        pythia8PSweightsSettingsBlock,
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CUEP8M1Settings',
                                    'pythia8aMCatNLOSettings',
                                    'pythia8PSweightsSettings'
                                    )
    )
)

from PhysicsTools.HepMCCandAlgos.genParticles_cfi import genParticles
from PhysicsTools.JetMCAlgos.TauGenJets_cfi import tauGenJets
from PhysicsTools.JetMCAlgos.TauGenJetsDecayModeSelectorAllHadrons_cfi import tauGenJetsSelectorAllHadrons

genParticles.src = cms.InputTag("generator", "unsmeared")

tauGenJets.GenParticles = cms.InputTag("genParticles")
tauGenJets.includeNeutrinos = cms.bool(False)

genVisTauSelector = cms.EDFilter("CandViewSelector",
    src = cms.InputTag("tauGenJetsSelectorAllHadrons"),
    cut = cms.string("pt > 18")
  )             
        
genVisTauFilter = cms.EDFilter("CandViewCountFilter",
     src = cms.InputTag("genVisTauSelector"),
     minNumber = cms.uint32(1),
  )

ProductionFilterSequence = cms.Sequence(generator*genParticles*tauGenJets*tauGenJetsSelectorAllHadrons*genVisTauSelector*genVisTauFilter)


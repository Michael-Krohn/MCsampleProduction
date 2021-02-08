import FWCore.ParameterSet.Config as cms

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
	args = cms.vstring("###GRIDPACK###"),
        nEvents = cms.untracked.uint32(10000),
        numberOfParameters = cms.uint32(1),
        outputFile = cms.string('cmsgrid_final.lhe'),
        scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)
